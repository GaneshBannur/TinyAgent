import sys
sys.path.append('C:\\Users\\Bhavik Chandna\\Downloads\\ToolRAG_v2\\TinyAgent')

if __name__=="__main__":
    from argparse import ArgumentParser
    import asyncio

    from src.tiny_agent.tiny_agent import TinyAgentNoReplanning
    from src.tiny_agent.config import get_tiny_agent_config

    arg_parser = ArgumentParser()
    arg_parser.add_argument("--config_path", type=str, required=True)
    args = arg_parser.parse_args()

    tiny_agent_config = get_tiny_agent_config(config_path=args.config_path)
    tiny_agent = TinyAgentNoReplanning(tiny_agent_config)

    response = asyncio.run(
        tiny_agent.arun(query="Send a summary of the PDF document \"BusinessProposal.pdf\" to Alex and Sarah, then create a new note titled \"Lesson Calendar\" in the \"Work\" folder with the list points.")
        )
    print(response)
