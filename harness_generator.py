import os
import glob
import json
import urllib.request

# Configuration
DRIVER_DIR = "/workspaces/arm-mali-r54p0/arm-mali-r54p0-x86/downloads/driver/product/kernel"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:7b" # Or change to deepseek-coder:6.7b

def get_kernel_headers(directory):
    # Search recursively for all ioctl and kbase header files in the Mali source
    headers = glob.glob(os.path.join(directory, "**/*ioctl*.h"), recursive=True)
    headers += glob.glob(os.path.join(directory, "**/mali_kbase*.h"), recursive=True)
    return list(set(headers)) # remove duplicates

def query_ollama(prompt):
    data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    req = urllib.request.Request(
        OLLAMA_URL, 
        data=json.dumps(data).encode('utf-8'), 
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode('utf-8'))
        return res['response']

def main():
    print("[*] Scanning Mali driver directory for relevant C headers...")
    files = get_kernel_headers(DRIVER_DIR)
    
    if not files:
        print("[!] No matching header files found. Verify the DRIVER_DIR path.")
        return

    combined_code = ""
    for f_path in files:
        print(f"[+] Reading: {os.path.basename(f_path)}")
        try:
            with open(f_path, 'r', errors='ignore') as f:
                combined_code += f"\n/* File: {os.path.basename(f_path)} */\n" + f.read()
        except Exception as e:
            print(f"[!] Error reading {f_path}: {e}")

    # Limit code size to prevent context blowing out if files are massive
    if len(combined_code) > 100000:
        print("[!] Code context is very large. Truncating to fit model boundaries...")
        combined_code = combined_code[:100000]

    system_instruction = (
        "Act as an expert Linux kernel security tool. Generate a clean, syntax-valid Syzkaller "
        "interface description (Syzlang) based on the provided Mali GPU kernel driver structures. "
        "Identify the ioctl commands, struct layouts, and device path (/dev/mali0). "
        "Output ONLY valid Syzlang syntax wrapped inside a markdown code block. Do not write explanations.\n\n"
        f"Mali Driver Code:\n{combined_code}"
    )

    print(f"[*] Sending driver data to Ollama ({MODEL_NAME}). Please wait...")
    output = query_ollama(system_instruction)
    
    with open("mali_automated_harness.txt", "w") as out_file:
        out_file.write(output)
        
    print("[+] Successfully generated: mali_automated_harness.txt")

if __name__ == "__main__":
    main()
