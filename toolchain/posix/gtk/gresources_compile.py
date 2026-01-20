#!/usr/bin/env python3
import argparse
import itertools
import os
from pathlib import Path
import shutil
import subprocess

def get_files_by_patterns(directory_path:str, patterns:list[str], recursive:bool=True):
  """
  Finds all files in the given directory matching any of the patterns.

  Args:
      directory_path (str or Path): The directory to search in.
      patterns (list): A list of glob-style patterns (e.g., ['*.txt', '*.csv']).
      resursive (bool): If true, conduct a recursive search

  Returns:
      list: A list of Path objects for the matching files.
  """
  p = Path(directory_path)
  # Generate a sequence of matching files for each pattern, then chain them
  if recursive:
    func = p.rglob
  else:
    func = p.glob
  matched_files = itertools.chain.from_iterable(func(pattern) for pattern in patterns)
  # Convert the generator to a list, optionally filtering out directories if patterns match both
  return [file for file in matched_files if file.is_file()]

def main():
  # All arguments are positional
  parser = argparse.ArgumentParser(description="Compile gresources")
  parser.add_argument("target_source_dir", help="Absolute path of target source")
  parser.add_argument("gresources_path_rel", help="Path of gresources file relative to source root")
  parser.add_argument("target_gen_dir", help="Absolute path of target generated file directory")

  args = parser.parse_args()
  gresources_path = os.path.join(args.target_source_dir, args.gresources_path_rel)
  file_patterns = ["*.blp", "*.ui"]
  source_tree_ui_file_pathlib_paths = get_files_by_patterns(os.path.dirname(gresources_path), file_patterns)
  
  dependency_set:set[str] = set()
  blp_file_list:list[str] = []

  for source_tree_ui_file_pathlib_path in source_tree_ui_file_pathlib_paths:
    source_tree_ui_file_path = source_tree_ui_file_pathlib_path.as_posix()
    source_tree_ui_file_dir = source_tree_ui_file_pathlib_path.parent.as_posix()
    dependency_set.update({source_tree_ui_file_path, source_tree_ui_file_dir})

    # Add corresponding paths for generated files.
    # For example, <target_source_dir>/resources/something.ui maps to <target_gen_dir>/resources/something.ui
    # blp files are compiled to xml, in which case <target_source_dir>/resources/something.blp -> <target_gen_dir>/resources/something.ui
    target_source_dir_strlen = len(args.target_source_dir)
    ui_file_path_rel = source_tree_ui_file_path[target_source_dir_strlen:]
    copy_file = True

    if ui_file_path_rel[-3:] == "blp":
      ui_file_path_rel = ui_file_path_rel[:-3] + "ui"
      copy_file = False
      blp_file_list.append(source_tree_ui_file_path)

    gen_tree_ui_file_path = os.path.join(args.target_gen_dir, ui_file_path_rel)
    gen_tree_ui_file_dir = os.path.dirname(gen_tree_ui_file_path)
    dependency_set.update({gen_tree_ui_file_path, gen_tree_ui_file_dir})
    
    if copy_file:
      os.makedirs(gen_tree_ui_file_dir, exist_ok=True)
      shutil.copyfile(source_tree_ui_file_path, gen_tree_ui_file_path)

  compiled_gresources_path = os.path.join(args.target_gen_dir, args.gresources_path_rel) + ".c"
  dep_file_path = os.path.join(args.target_gen_dir, args.gresources_path_rel) + ".d"
  os.makedirs(os.path.dirname(dep_file_path), exist_ok=True)

  with open(dep_file_path, "w") as file:
    dep_file_content_parts:list[str] = [ compiled_gresources_path, ":" ]
    for dependency in dependency_set:
      dep_file_content_parts.append(dependency)

    dep_file_content = " ".join(dep_file_content_parts)
    file.write(dep_file_content)

  # Run blueprint compiler
  if len(blp_file_list) > 0:
    blueprint_compile_command = [ "blueprint-compiler", "batch-compile", args.target_gen_dir, args.target_source_dir ] + blp_file_list
    result = subprocess.run(blueprint_compile_command)
    result.check_returncode()

  # Run gresources compiler
  compiled_gresources_dir = os.path.dirname(compiled_gresources_path)
  gresources_compile_command = [ "glib-compile-resources", "--sourcedir", compiled_gresources_dir, "--target", compiled_gresources_path, "--generate-source", gresources_path ]
  result = subprocess.run(gresources_compile_command)
  result.check_returncode()


if __name__ == "__main__":
  main()