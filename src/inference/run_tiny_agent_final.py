import sys
sys.path.append('C:\\Users\\Bhavik Chandna\\Downloads\\ToolRAG_v2\\TinyAgent')
import asyncio
import pandas as pd
from argparse import ArgumentParser
from tqdm import tqdm
from src.tiny_agent.tiny_agent import TinyAgentNoReplanning
from src.tiny_agent.config import get_tiny_agent_config

def convert_model_response(model_response):
    result = {}
    for task in model_response.values():
        if isinstance(task, dict) and 'name' in task and 'args' in task:
            result[task['name']] = list(task['args'])
        elif hasattr(task, 'name') and hasattr(task, 'args'):
            result[task.name] = list(task.args)
    return result

async def process_queries(tiny_agent, queries):
    results = []
    for query_1 in tqdm(queries, desc="Processing queries", unit="query"):
        try:
            response = await tiny_agent.arun(query=query_1)
            print(query_1)
            converted_response = convert_model_response(response)
            print(converted_response)
            results.append({'input': query_1, 'tool_outputs': converted_response})
        except Exception as e:
            print(f"Error processing query '{query_1}': {e}")
            results.append({'input': query_1, 'tool_outputs': f"Error: {e}"})
    return results


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--config_path", type=str, required=True)
    args = arg_parser.parse_args()

    tiny_agent_config = get_tiny_agent_config(config_path=args.config_path)
    tiny_agent = TinyAgentNoReplanning(tiny_agent_config)

    # Read input queries from output_dataset.csv
    input_df = pd.read_csv('output_dataset_final.csv')
    input_df = input_df[0:512]
    input_queries = input_df['Inputs'].tolist()

    print(f"Processing {len(input_queries)} queries...")

    # Process all queries
    results = asyncio.run(process_queries(tiny_agent, input_queries))

    # Create DataFrame from results
    output_df = pd.DataFrame(results)
    output_path = 'model_inference_v4.csv'
    # Save to model_inference.csv
    output_df.to_csv(output_path, index=False)

    print(f"Model inference results have been saved to {output_path}")