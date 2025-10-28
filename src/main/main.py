from backend.config import Config
from backend.factory import DataFactory
from backend.correlation import get_correlation, shapiro_wilk, cramers_v
import os

def main():
    c = Config()
    b = c.config.get("data_backend")
    

    main_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(main_dir, '../results')

    for run_cfg in c.config.get("run", []):

        data_files = run_cfg.get("data_files", [])
        dataframes = {}  # ← aqui guardamos os dataframes com seus labels

        name = run_cfg.get("name")
        print(f"\n🔍 Executing analysis: {name}")

        analyses = run_cfg.get("analyses", {})

        for file_entry in data_files:
            file_name, file_type, label, sep = file_entry
            print(f"  - Loading file: {file_name} (tipo: {file_type}, label: {label})")
            df = DataFactory(b, file_type, file_name, sep)
            print(f"  - Dataframe summary:")
            print(df.summary())
            dataframes[label] = df.df     

            for analysis_name, analysis_cfg in analyses.items():
                
                if not analysis_cfg.get("enabled", False):
                    continue

                print(f"  ▶ Analysis: {analysis_name}")

                #-------------------------------------------------------
                # Correlation
                #-------------------------------------------------------
                if analysis_name == "correlation":
                    
                    output_path = os.path.join(results_dir, "correlation")
                    os.makedirs(output_path, exist_ok=True)
                    fileout = label + "_correlation.txt"
                    filepath = os.path.join(output_path, fileout)

                    attributes = analysis_cfg.get("attributes", [])
                    with open(filepath, "w") as f:
                        for attr in attributes:
                            attr_name, attr_type, target_name, target_type, method = attr
                            print(f"correlation:   - {attr_name:10s} ({attr_type}) → {target_name} ({target_type})")    
                            result = get_correlation(dataframes[label], attr_name, target_name, attr_type, target_type, method)

                            if result["method"] in ("Spearman", "Pearson", "Point Biserial"):
                                f.write(
                                    f"Attribute: {attr_name}, Target: {target_name}, "
                                    f"Method: {result['method']}, "
                                    f"Correlation: {result['value']:.4f}, "
                                    f"P-value: {result['p-value']:.4e}\n"
                                )
                            elif result["method"] == "Eta":
                                f.write(
                                    f"Attribute: {attr_name}, Target: {target_name}, "
                                    f"Method: {result['method']}, "
                                    f"Correlation: {result['value']:.4f}\n"
                                )
                                
                #-------------------------------------------------------
                #  Cramers V
                #-------------------------------------------------------   
                if analysis_name == "cramers_v":
                    output_path = os.path.join(results_dir, "cramers_v")
                    os.makedirs(output_path, exist_ok=True)
                    fileout = label + "_crammers_v.txt"
                    filepath = os.path.join(output_path, fileout) 
                    
                    attributes = analysis_cfg.get("attributes", [])  
                    
                    with open(filepath, "w") as f:
                        for attr in attributes:
                            attr1, attr2 = attr
                            print(f"cramers_v:   - {attr1:10s} ({attr2:10s})")    
                            result = cramers_v(dataframes[label], attr1, attr2)
                            
                            f.write(
                                f"Attribute: {attr1}, "
                                f"Attribute: {attr2}, "
                                f"Method: Cramers V, "
                                f"Result: {result}\n "
                            )                                        
                                                
                    
                #-------------------------------------------------------
                # Shapiro Wilk
                #-------------------------------------------------------    
                if analysis_name == "shapiro_wilk":
                    output_path = os.path.join(results_dir, "shapiro_wilk")
                    os.makedirs(output_path, exist_ok=True)
                    fileout = label + "_shapiro_wilk.txt"
                    filepath = os.path.join(output_path, fileout)   
                    
                    attributes = analysis_cfg.get("attributes", [])  

                    with open(filepath, "w") as f:
                        for attr in attributes:
                            attr_name, p_value = attr
                            print(f"shapiro_wilk:   - {attr_name:10s} ({p_value})")    
                            result = shapiro_wilk(dataframes[label], attr_name, p_value)

                            f.write(
                                f"Attribute: {attr_name}, "
                                f"Method: Shapiro-Wilk, "
                                f"Correlation: {result['Estatística W']:.4f}, "
                                f"P-value: {result['p-value']:.4e}, "
                                f"Significance: {result['significance']}, "
                                f"Interpretação: {result['Interpretação']},\n"
                            )                                        

if __name__ == "__main__":
    main()