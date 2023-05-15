import os


def python_submit(command, node=None, ngpus=0):
    if not os.path.exists("./slurm"):
        os.makedirs("./slurm")
    bash_file = open("./slurm.sh", "w")
    bash_file.write(f"#!/bin/bash\n{command}")
    bash_file.close()
    if node is None:
        os.system(
            f"sbatch --gres=gpu:{ngpus} --output ./slurm/slurm-%j.out"
            f"--mem=256000 --time=100-00:00:00 slurm.sh"
        )
    else:
        os.system(
            f"sbatch --gres=gpu:{ngpus} --output ./slurm/slurm-%j.out"
            f"--mem=256000 --nodelist={node} --time=100-00:00:00 slurm.sh"
        )
    os.remove("./slurm.sh")
