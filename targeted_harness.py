import os
import json
import urllib.request

# Configuration
DRIVER_DIR = "/workspaces/arm-mali-r54p0/arm-mali-r54p0-x86/downloads/driver/product/kernel"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:7b"

def find_target_headers(directory):
    targets = ["mali_kbase_ioctl.h", "mali_kbase_csf_ioctl.h"]
    found_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file in targets:
                found_files.append(os.path.join(root, file))
    return found_files

def query_ollama(prompt):
    data = {"model": MODEL_NAME, "prompt": prompt, "stream": False}
    req = urllib.request.Request(
        OLLAMA_URL, 
        data=json.dumps(data).encode('utf-8'), 
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode('utf-8'))
        return res['response']

def main():
    print("[*] Filtering directly for Mali entry point ioctl headers...")
    files = find_target_headers(DRIVER_DIR)
    
    if not files:
        print("[!] Target ioctl header files not found. Check directory structures.")
        return

    combined_code = ""
    for f_path in files:
        print(f"[+] Loading core target: {f_path}")
        with open(f_path, 'r', errors='ignore') as f:
            combined_code += f"\n/* File: {os.path.basename(f_path)} */\n" + f.read()

    system_instruction = (
        "Act as an expert Linux kernel security tool. Generate a clean, syntax-valid Syzkaller "
        "interface description (Syzlang) based on the provided Mali GPU kernel driver structures. "
        "Identify the ioctl commands, struct layouts, and device path (/dev/mali0).\n\n"
        "Output Requirements:\n"
        "- Provide ONLY valid Syzkaller syntax (.txt format).\n"
        "- Explicitly map structures using Syzkaller primitives.\n"
        "- Define open, mmap, and ioctl calls.\n"
        "- Do not include conversational text outside markdown code blocks.\n\n"
        f"Mali Driver Code:\n{combined_code}"
    )

    print(f"[*] Dispatching data to Ollama ({MODEL_NAME}). This will run quickly now...")
    output = query_ollama(system_instruction)
    
    with open("mali_automated_harness.txt", "w") as out_file:
        out_file.write(output)
        
    print("[+] Successfully generated: mali_automated_harness.txt")

if __name__ == "__main__":
    main()
