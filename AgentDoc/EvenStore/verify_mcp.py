import asyncio,json
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
ROOT=Path(__file__).resolve().parents[2]
async def probe(name,cmd,args,call=None):
 async with stdio_client(StdioServerParameters(command=cmd,args=args)) as (r,w):
  async with ClientSession(r,w) as session:
   init=await asyncio.wait_for(session.initialize(),20); listing=await asyncio.wait_for(session.list_tools(),20)
   result={'server':name,'initialize':'PASS','tools':len(listing.tools),'server_info':init.serverInfo.model_dump()}
   if call:
    response=await asyncio.wait_for(session.call_tool(*call),20)
    result['call']={'name':call[0],'is_error':response.isError,'content':[c.model_dump() for c in response.content]}
   return result
async def main():
 results=[]
 results.append(await probe('symdex-py-networksimulator','/home/tonywang/miniforge3/bin/symdex',['--state-dir',str(ROOT/'AgentDoc/tool-state/symdex'),'serve']))
 results.append(await probe('filesystem-py-networksimulator','/usr/local/bin/mcp-server-filesystem',[str(ROOT)],('list_allowed_directories',{})))
 (ROOT/'AgentDoc/EvenStore/mcp-smoke.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(results,ensure_ascii=False))
asyncio.run(main())
