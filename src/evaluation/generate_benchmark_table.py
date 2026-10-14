import json
import os
import pandas as pd

def load_metrics(metrics_dir: str = "reports/metrics") -> dict:
    files = {
        "tier1": "tier1_lexicon.json",
        "tier2": "tier2_classical_ml.json",
        "zero_shot": "finbert_zero_shot.json",
        "fine_tuned": "finbert_fine_tuned.json",
        "entity_aware": "finbert_entity_aware.json",
    }
    data = {}
    for key, fname in files.items():
        path = os.path.join(metrics_dir, fname)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data[key] = json.load(f)
    return data

def build_benchmark_dataframe(metrics_dir: str = "reports/metrics") -> pd.DataFrame:
    raw = load_metrics(metrics_dir)
    records = []

    # 1. Tier 1: Lexicon
    if "tier1" in raw:
        t1 = raw["tier1"]
        rep = t1.get("classification_report", {})
        records.append({
            "Paradigm": "Tier 1: Lexicon",
            "Model": "Loughran-McDonald",
            "Accuracy": t1.get("accuracy", 0.0),
            "Macro Precision": rep.get("macro avg", {}).get("precision", 0.0),
            "Macro Recall": rep.get("macro avg", {}).get("recall", 0.0),
            "Macro F1": t1.get("macro_f1", 0.0),
            "Weighted F1": t1.get("weighted_f1", 0.0),
        })

    # 2. Tier 2: Classical ML
    if "tier2" in raw:
        t2 = raw["tier2"]
        name_map = {
            "Multinomial_Naive_Bayes": "Multinomial NB",
            "Logistic_Regression": "Logistic Regression",
            "Linear_SVM": "Linear SVM"
        }
        for k, v in t2.items():
            rep = v.get("classification_report", {})
            records.append({
                "Paradigm": "Tier 2: Classical ML",
                "Model": name_map.get(k, k),
                "Accuracy": v.get("test_accuracy", 0.0),
                "Macro Precision": rep.get("macro avg", {}).get("precision", 0.0),
                "Macro Recall": rep.get("macro avg", {}).get("recall", 0.0),
                "Macro F1": v.get("test_macro_f1", 0.0),
                "Weighted F1": v.get("test_weighted_f1", 0.0),
            })

    # 3. Tier 3: Pretrained Transformers (Zero-shot)
    if "zero_shot" in raw:
        zs = raw["zero_shot"]
        for m_name, v in zs.items():
            rep = v.get("classification_report", {})
            label = "FinBERT Zero-Shot (ProsusAI)" if "ProsusAI" in m_name else "FinBERT Zero-Shot (HKUST)"
            records.append({
                "Paradigm": "Tier 3: Transformer (ZS)",
                "Model": label,
                "Accuracy": v.get("accuracy", 0.0),
                "Macro Precision": rep.get("macro avg", {}).get("precision", 0.0),
                "Macro Recall": rep.get("macro avg", {}).get("recall", 0.0),
                "Macro F1": v.get("macro_f1", 0.0),
                "Weighted F1": v.get("weighted_f1", 0.0),
            })

    # 4. Tier 3: FinBERT Fine-Tuned
    if "fine_tuned" in raw:
        ft = raw["fine_tuned"]
        rep = ft.get("classification_report", {})
        records.append({
            "Paradigm": "Tier 3: Transformer (FT)",
            "Model": "FinBERT Fine-Tuned (HKUST)",
            "Accuracy": ft.get("test_accuracy", 0.0),
            "Macro Precision": rep.get("macro avg", {}).get("precision", 0.0),
            "Macro Recall": rep.get("macro avg", {}).get("recall", 0.0),
            "Macro F1": ft.get("test_macro_f1", 0.0),
            "Weighted F1": ft.get("test_weighted_f1", 0.0),
        })

    # 5. Extension: Entity-Aware FinBERT (SEntFiN 1.0)
    if "entity_aware" in raw:
        ea = raw["entity_aware"]
        rep = ea.get("classification_report", {})
        records.append({
            "Paradigm": "Extension: Entity-Aware",
            "Model": "Entity-FinBERT (SEntFiN 1.0)",
            "Accuracy": ea.get("test_accuracy", 0.0),
            "Macro Precision": rep.get("macro avg", {}).get("precision", 0.0),
            "Macro Recall": rep.get("macro avg", {}).get("recall", 0.0),
            "Macro F1": ea.get("test_macro_f1", 0.0),
            "Weighted F1": ea.get("test_weighted_f1", 0.0),
        })

    return pd.DataFrame(records)

def export_tables(df: pd.DataFrame, out_dir: str = "reports/tables"):
    os.makedirs(out_dir, exist_ok=True)
    
    # 1. Export CSV
    csv_path = os.path.join(out_dir, "benchmark_results.csv")
    df.to_csv(csv_path, index=False)
    
    # 2. Export Markdown Table
    md_path = os.path.join(out_dir, "benchmark_results.md")
    # Định dạng % hiển thị 4 chữ số thập phân
    display_df = df.copy()
    for col in ["Accuracy", "Macro Precision", "Macro Recall", "Macro F1", "Weighted F1"]:
        display_df[col] = display_df[col].apply(lambda x: f"{x:.4f}")
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Master Scientific Benchmark Results\n\n")
        f.write(display_df.to_markdown(index=False))
        f.write("\n")

    # 3. Export IEEE LaTeX Table
    tex_path = os.path.join(out_dir, "benchmark_results.tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write("% IEEE 2-Column Format Table\n")
        f.write("\\begin{table*}[t]\n")
        f.write("\\centering\n")
        f.write("\\caption{Comparative Performance Benchmark Across NLP Paradigms on Financial PhraseBank (75\\% Agreement) and SEntFiN 1.0 Test Splits.}\n")
        f.write("\\label{tab:benchmark_results}\n")
        f.write("\\begin{tabular}{llccccc}\n")
        f.write("\\toprule\n")
        f.write("\\textbf{Paradigm} & \\textbf{Model} & \\textbf{Accuracy} & \\textbf{Macro P} & \\textbf{Macro R} & \\textbf{Macro F1} & \\textbf{Weighted F1} \\\\\n")
        f.write("\\midrule\n")
        
        current_paradigm = ""
        for _, row in display_df.iterrows():
            paradigm = row["Paradigm"] if row["Paradigm"] != current_paradigm else ""
            current_paradigm = row["Paradigm"]
            f.write(f"{row['Paradigm']} & {row['Model']} & {row['Accuracy']} & {row['Macro Precision']} & {row['Macro Recall']} & {row['Macro F1']} & {row['Weighted F1']} \\\\\n")
            
        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n")
        f.write("\\end{table*}\n")

    print(f"[✓] Đã xuất thành công:\n - {csv_path}\n - {md_path}\n - {tex_path}")

if __name__ == "__main__":
    df = build_benchmark_dataframe()
    export_tables(df)