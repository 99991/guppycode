#!/usr/bin/env python
import json, time, tabcompletion, tools, sound, llm, prn, sessions
from config import args

tabcompletion.activate()

session = sessions.Session(args.session)
session.append({"role": "system", "content": args.system_prompt})
cost, total_cost, tokens = 0, 0, 0

def info(msg):
    prn.green(msg)
    if tokens:
        prn.green(f"Cost: ${cost:.6f}, Total: ${total_cost:.6f}, Tokens: {tokens}")

while True:
    try:
        prompt = input(">> ") if args.prompt is None else args.prompt
    except (KeyboardInterrupt, EOFError): break

    session.append({"role": "user", "content": prompt})

    start = time.perf_counter()

    try:
        for step in range(args.max_steps):
            info(f"Step {step + 1}")

            response = llm.call_llm(session.get_messages())

            if "usage" in response:
                tokens = response["usage"].get("total_tokens", 0)
                cost = response["usage"].get("cost", 0)
                total_cost += cost

            msg = response["choices"][0]["message"]

            # Append assistant message
            session.append(msg)

            tool_calls = msg.get("tool_calls")

            # If no tools -> final answer
            if not tool_calls:
                if msg.get("content"):
                    info("Agent response")
                    print(msg["content"])
                break

            # Execute tools
            for tool_call in tool_calls:
                fn_name = tool_call["function"]["name"]
                tool_args = json.loads(tool_call["function"]["arguments"])
                tool_call_id = tool_call["id"]

                prn.orange(f"Tool call: {fn_name}, {json.dumps(tool_args, indent=4)}")

                if fn_name in tools.TOOL_MAP:
                    result = tools.TOOL_MAP[fn_name](tool_args)
                else:
                    result = f"Unknown tool: {fn_name}"

                info("Tool output")
                prn.lightwhite(result)

                session.append({
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": result
                })

        else:
            prn.red(f"ERROR: Max steps of {args.max_steps} reached.")

    except KeyboardInterrupt: pass

    dt = time.perf_counter() - start
    info(f"Finished in {dt:.2f}s")

    sound.play_finish_sound()

    if args.prompt is not None: break

print("Quit")
