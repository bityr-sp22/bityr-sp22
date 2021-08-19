from argparse import ArgumentParser
import pickle

def setup_parser(parser: ArgumentParser):
  parser.add_argument("datasets", nargs='+', type=str)
  parser.add_argument("-o", "--output", type=str)
  parser.add_argument("-v", "--verbose", action="store_true")
  parser.add_argument("--no-dedup", action="store_true")

def main(args):
  # Variables
  total_of_datasets = 0
  merged_dataset = []
  visited_funcs = set()
  duplicated_funcs = set()

  # Iterate through all datasets
  for i, dataset_file_name in enumerate(args.datasets):
    if args.verbose:
      print(f"Processing dataset {i + 1}/{len(args.datasets)}: {dataset_file_name}")
    dataset = pickle.load(open(dataset_file_name, "rb"))
    total_of_datasets += len(dataset)

    # Record the functions visited in this current dataset
    current_visited_funcs = set()
    for entry in dataset:
      entry_input = entry[0]
      directory = entry_input.directory
      file_name = entry_input.file_name
      func_name = entry_input.function_name

      # Deal with No Deduplicate
      if args.no_dedup or directory is None or file_name is None or func_name is None:
        merged_dataset.append(entry)
        continue

      key = (directory, file_name, func_name)
      current_visited_funcs.add(key)

      # Check if the function is visited
      if not key in visited_funcs:

        # If not, add the datapoint into the merged dataset
        merged_dataset.append(entry)
      else:

        # Record the duplication
        duplicated_funcs.add(key)

    # Update the visited functions with all the current visited functions
    visited_funcs = visited_funcs.union(current_visited_funcs)

  # Finish prints
  size = len(merged_dataset)
  if args.verbose:
    print(f"Generated size: {size}, Total: {total_of_datasets}, #Duplicates: {total_of_datasets - size}, #Duplicated Funcs: {len(duplicated_funcs)}")

  # Dump the merged dataset
  pickle.dump(merged_dataset, open(args.output, "wb"))
