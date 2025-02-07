import argparse
import subprocess
import os

def get_free_gpu_memory():
    """Get the available GPU memory using nvidia-smi."""
    try:
        total_memory = subprocess.check_output(
            ["nvidia-smi", "--id=0", "--query-gpu=memory.total", "--format=csv,noheader,nounits"]
        ).decode("utf-8").strip()
        used_memory = subprocess.check_output(
            ["nvidia-smi", "--id=0", "--query-gpu=memory.used", "--format=csv,noheader,nounits"]
        ).decode("utf-8").strip()
        free_memory = int(total_memory) - int(used_memory)
        return free_memory
    except Exception as e:
        print(f"Error fetching GPU memory: {e}")
        return 4096  # Default to 4GB if there's an issue

def generate_trt_engine(onnx_file, image_size, generate_graph):
    workspace = get_free_gpu_memory()
    stride = 32
    network_size = image_size + stride
    shape = f"1x3x{network_size}x{network_size}"
    file_no_ext = os.path.splitext(onnx_file)[0]
    trt_engine = f"{file_no_ext}.engine"
    graph = f"{trt_engine}.layer.json"
    profile = f"{trt_engine}.profile.json"
    timing = f"{trt_engine}.timing.json"
    timing_cache = f"{trt_engine}.timing.cache"
    
    cmd = [
        "trtexec", "--onnx", onnx_file,
        "--saveEngine", trt_engine,
        "--fp16", "--int8",
        "--useCudaGraph",
        "--minShapes=images:" + shape,
        "--optShapes=images:" + shape,
        "--maxShapes=images:" + shape,
        f"--memPoolSize=workspace:{workspace}MiB",
        "--timingCacheFile", timing_cache
    ]
    
    if generate_graph:
        cmd.extend([
            "--separateProfileRun",
            "--useSpinWait",
            "--profilingVerbosity=detailed",
            "--dumpLayerInfo",
            "--exportTimes", timing,
            "--exportLayerInfo", graph,
            "--exportProfile", profile
        ])
    
    print("Executing command:", " ".join(cmd))
    result = subprocess.run(cmd, shell=True)
    
    if result.returncode == 0:
        print(f"Engine file generated successfully: {trt_engine}")
        if generate_graph:
            print(f"Graph file generated successfully: {graph}")
            print(f"Profile file generated successfully: {profile}")
    else:
        print("Failed to generate engine file.")
        exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate TensorRT Engine from ONNX file.")
    parser.add_argument("onnx_file", type=str, help="Path to the input ONNX file")
    parser.add_argument("image_size", type=int, help="Image size for inference")
    parser.add_argument("--generate-graph", action="store_true", help="Enable graph generation")
    
    args = parser.parse_args()
    generate_trt_engine(args.onnx_file, args.image_size, args.generate_graph)
