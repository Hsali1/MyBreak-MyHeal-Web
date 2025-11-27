import sys
import os


def break_it(source, prefix, chunk_size, destination):
    print(f"Source = {source}")
    print(f"prefix = {prefix}")
    print(f"chunk_size = {chunk_size}")
    print(f"destination = {destination}")
    # convert kilobytes (kb) into bytes
    chunk_size = 1024 * int(chunk_size)
    # chunk_size needs to be between 1 kb and 1 gb
    if chunk_size <= 0 or chunk_size > (1024 * 1024 * 1024):
        print(f"Chunk size error. {chunk_size} needs to be between 1 (1 KB)"
              f"and {1024 * 1024 * 1024} (1 GB)")
        sys.exit(1)
    try:
        with open(source, "rb") as f:
            i = 0
            while True:
                # file_name = prefix.32 numbers including i
                # example Prefix.00000000000000000000000000000005
                file_name = f"{prefix}.{str(i).zfill(32)}"
                chunk_path = os.path.join(destination, file_name)
                with open(chunk_path, "wb") as tf:
                    print(f"Writing {file_name}")
                    # read from f and write to tf, 8 bytes at a time
                    # each time a loop is iterated the file pointer moves 8 byt
                    for _ in range(chunk_size // 8):
                        ccc = f.read(8)
                        if not ccc:
                            print(f"done... {i+1} chunks produced for {source}")
                            sys.exit(0)
                        tf.write(ccc)
                i += 1
    except FileNotFoundError:
        print(f"file {source} can not be opened...")
    return 1


def heal_it(target, prefix, chunk_size, number_of_chunks):
    # make sure chunks are valid
    if (number_of_chunks <= 0) or (number_of_chunks > (8192 * 16)):
        print(f"Chunks error. {number_of_chunks} needs to be between 1 "
              f"and {8192 * 16}")
        sys.exit(1)

    # convert chunks from KB to B
    chunk_size = chunk_size * 1024
    if chunk_size <= 0 or chunk_size > (1024 * 1024 * 1024):
        print(f"Chunk size error. {chunk_size} needs to be between 1 (1 KB)"
              f"and {1024 * 1024 * 1024} (1 GB)")
        sys.exit(1)

    try:
        with open(target, "wb") as output_file:
            for i in range(number_of_chunks):
                chunk_file_name = f"{prefix}.{str(i).zfill(32)}"
                with open(chunk_file_name, "rb") as chunk_file:
                    chunk_data = chunk_file.read()
                    output_file.write(chunk_data)
                    print(f"Chunk {i + 1} merged successfully")
            print("All chunks merged successfully")
    except FileNotFoundError:
        print(f"file {target} can not be opened...")
        sys.exit(1)
