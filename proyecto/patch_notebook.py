import json

with open("/home/jsr-mario/raid/Documents/School/semestre_8/cuantica_2/proyecto/SosaJuan_ComputacionCuantica2_Proyecto.ipynb", "r") as f:
    nb = json.load(f)

# 1. Replace 'bind_parameters' with 'assign_parameters' in all cells
for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        new_source = []
        for line in cell["source"]:
            new_source.append(line.replace("bind_parameters", "assign_parameters"))
        cell["source"] = new_source

# 2. Add Histogram cell under "### Ideal vs con ruido"
def create_code_cell(source):
    if isinstance(source, str):
        source = [source]
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [s + "\n" if not s.endswith("\n") else s for s in source]
    }

def find_header(text):
    for i, cell in enumerate(nb["cells"]):
        if cell["cell_type"] == "markdown":
            src = "".join(cell["source"])
            if text in src:
                return i
    return -1

idx_histogram = find_header("### Ideal vs con ruido")
if idx_histogram != -1:
    # Check if we already inserted it
    if idx_histogram + 1 < len(nb["cells"]) and "plot_histogram" in "".join(nb["cells"][idx_histogram + 1].get("source", [])):
        pass # Already added
    else:
        nb["cells"].insert(idx_histogram + 1, create_code_cell([
            "from qiskit.visualization import plot_histogram",
            "",
            "# Simulamos un caso ruidoso específico para compararlo directamente con el ideal",
            "p_example = 0.02",
            "nm_example = build_noise_model(p_example, 'depolarizing')",
            "rho_example = run_noisy_qaoa(nm_example, opt_params_ideal)",
            "",
            "# Extraemos las probabilidades de los estados (diccionario)",
            "probs_ideal = state_ideal.probabilities_dict()",
            "probs_noisy = rho_example.probabilities_dict()",
            "",
            "# Como tenemos 9 qubits (512 estados), filtramos solo los 10 más probables del caso ideal",
            "def top_k_dict(d_ideal, d_noisy, k=10):",
            "    sorted_keys = sorted(d_ideal.keys(), key=lambda x: d_ideal[x], reverse=True)[:k]",
            "    return {k: d_ideal[k] for k in sorted_keys}, {k: d_noisy.get(k, 0.0) for k in sorted_keys}",
            "",
            "top_ideal, top_noisy = top_k_dict(probs_ideal, probs_noisy, k=10)",
            "",
            "print(f\"Fidelidad entre estado Ideal y Ruidoso (p={p_example}): {state_fidelity(rho_ideal, rho_example):.4f}\")",
            "",
            "plot_histogram([top_ideal, top_noisy], legend=['Ideal', 'Con Ruido (Depolarizing p=0.02)'],",
            "               title='Comparación de Probabilidades de Medición (Top 10 estados)',",
            "               figsize=(12, 6))"
        ]))

with open("/home/jsr-mario/raid/Documents/School/semestre_8/cuantica_2/proyecto/SosaJuan_ComputacionCuantica2_Proyecto.ipynb", "w") as f:
    json.dump(nb, f, indent=2)

print("Notebook patched successfully!")
