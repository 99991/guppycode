#!/usr/bin/env python
import json, time, tabcompletion, tools, sound, llm, prn
from config import args

tabcompletion.activate()

messages = [{"role": "system", "content": args.system_prompt}]
total_cost = 0.0

while True:
    try:
        prompt = input(">> ") if args.prompt is None else args.prompt
    except (KeyboardInterrupt, EOFError): break

    messages.append({"role": "user", "content": prompt})

    start = time.perf_counter()

    try:
        for step in range(args.max_steps):
            prn.green(f"Step {step + 1}")

            response = llm.call_llm(messages)

            print(json.dumps(response, indent=4))

            if "cost" in response["usage"]:
                cost = response["usage"]["cost"]
                total_cost += cost
                prn.green(f"Cost: ${cost:.6f}, Total: ${total_cost:.6f}")

            msg = response["choices"][0]["message"]

            # Append assistant message
            messages.append(msg)

            tool_calls = msg.get("tool_calls")

            # If no tools -> final answer
            if not tool_calls:
                if msg.get("content"):
                    prn.green("Agent response:")
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

                prn.green("Tool output:")
                prn.lightwhite(result)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": result
                })

        else:
            prn.red(f"ERROR: Max steps of {args.max_steps} reached.")

    except KeyboardInterrupt: pass

    dt = time.perf_counter() - start
    prn.green(f"Finished in {dt:.2f}s")

    sound.play_finish_sound()

    if args.prompt is not None: break

print("Quit")
