import json
import argparse
from agents.data_gatherer import DataGatherer

def main():
    parser = argparse.ArgumentParser(description="Run the data gatherer script.")
    parser.add_argument("--topic", type=str, required=True, help="The topic to gather data for.")
    parser.add_argument("--source", type=str, required=False, default="news", help="The source to gather data from news, google, youtube, or all.")
    args = parser.parse_args()

    data_gatherer = DataGatherer()
    
    if args.source == "news":
        all_data = data_gatherer.gather_newsapi_data_and_summarize_sources(args.topic)
    elif args.source == "google":
        print(f"The source '{args.source}' is not available.")
        return 
        all_data = data_gatherer.gather_data_and_summarize_sources(args.topic)
    elif args.source == "youtube":
        print(f"The source '{args.source}' is not available.")
        return 
        # all_data = data_gatherer.gather_youtube_data_and_summarize(args.topic)
    elif args.source == "all":
        print(f"The source '{args.source}' is not available.")
        return
        # all_data = data_gatherer.gather_newsapi_data_and_summarize_sources(args.topic)

    # Save the results to a JSON file
    file_name = args.topic.replace(" ", "_") + "_results_with_summaries.json"
    with open("results/"+file_name, "w") as json_file:
        json.dump(all_data, json_file, indent=2)

    print("\nResults have been saved to " + file_name)

if __name__ == "__main__":
    main()