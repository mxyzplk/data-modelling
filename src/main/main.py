from backend.config import Config
from backend.factory import DataFactory

def main():
    c = Config()
    b = c.config.get("data_backend")
    
    data_files = run_cfg.get("data_files", [])
    dataframes = {}  # ← aqui guardamos os dataframes com seus labels

    for file_entry in data_files:
        file_name, file_type, label = file_entry
        print(f"  - Carregando arquivo: {file_name} (tipo: {file_type}, label: {label})")
        df = DataFactory(b, file_type, file_name)
        dataframes[label] = df     


    for run_cfg in c.config.get("run", []):
        name = run_cfg.get("name")
        print(f"\n🔍 Executando análise: {name}")

        # Chega até o nível 'analyses'
        analyses = run_cfg.get("analyses", {})

        # Loop sobre cada tipo de análise dentro de 'analyses'
        for analysis_name, analysis_cfg in analyses.items():
            if not analysis_cfg.get("enabled", False):
                continue  # pula análises desativadas

            print(f"  ▶ Análise ativa: {analysis_name}")

            # Exemplo: se for correlação
            if analysis_name == "correlation":
                attributes = analysis_cfg.get("attributes", [])
                for attr in attributes:
                    attr_name, attr_type, target_name, target_type = attr
                    print(f"     - {attr_name:10s} ({attr_type}) → {target_name} ({target_type})")




if __name__ == "__main__":
    main()