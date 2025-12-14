import streamlit as st
import pandas as pd
import numpy as np

# Set up the page
st.set_page_config(
    page_title="WHO AWaRe Drug Classifier",
    page_icon="💊",
    layout="wide"
)

# Title and description
st.title("WHO AWaRe Antibiotic Classification")
st.markdown("""
This app classifies antibiotics into the WHO AWaRe categories (Access, Watch, Reserve) based on the 2023 WHO classification.
Select drugs from the list or upload a file to get their classification.
""")

# Sidebar for information
with st.sidebar:
    st.header("About AWaRe Classification")
    st.markdown("""
    **AWaRe Categories:**
    - **🟢 Access**: First or second choice empiric treatment options
    - **🟡 Watch**: Higher resistance potential, key stewardship targets
    - **🔴 Reserve**: "Last resort" for multidrug-resistant infections

    **EML Status:**
    - **🟢 Yes**: Included in WHO Essential Medicines List
    - **🔴 No**: Not included in WHO Essential Medicines List

    *Source: [WHO-MHP-HPS-EML-2023.04](https://www.who.int/publications/i/item/WHO-MHP-HPS-EML-2023.04)*
    """)

    st.divider()
    st.caption("Developed using WHO drug classification data")


# Create drug database from the provided data
def create_drug_database():
    """Create drug database from the provided Excel text content"""

    # Full list of drugs from the Excel file
    data = [
        # Format: Antibiotic, Class, ATC, Category, EML
        ["Amikacin", "Aminoglycosides", "J01GB06", "Access", "Yes"],
        ["Amoxicillin", "Penicillins", "J01CA04", "Access", "Yes"],
        ["Amoxicillin/clavulanic-acid", "Beta-lactam/beta-lactamase-inhibitor", "J01CR02", "Access", "Yes"],
        ["Ampicillin", "Penicillins", "J01CA01", "Access", "Yes"],
        ["Ampicillin/sulbactam", "Beta-lactam/beta-lactamase-inhibitor", "J01CR01", "Access", "No"],
        ["Arbekacin", "Aminoglycosides", "J01GB12", "Watch", "No"],
        ["Aspoxicillin", "Penicillins", "J01CA19", "Watch", "No"],
        ["Azidocillin", "Penicillins", "J01CE04", "Access", "No"],
        ["Azithromycin", "Macrolides", "J01FA10", "Watch", "Yes"],
        ["Azlocillin", "Penicillins", "J01CA09", "Watch", "No"],
        ["Aztreonam", "Monobactams", "J01DF01", "Reserve", "No"],
        ["Bacampicillin", "Penicillins", "J01CA06", "Access", "No"],
        ["Bekanamycin", "Aminoglycosides", "J01GB13", "Watch", "No"],
        ["Benzathine-benzylpenicillin", "Penicillins", "J01CE08", "Access", "Yes"],
        ["Benzylpenicillin", "Penicillins", "J01CE01", "Access", "Yes"],
        ["Biapenem", "Carbapenems", "J01DH05", "Watch", "No"],
        ["Brodimoprim", "Trimethoprim-derivatives", "J01EA02", "Access", "No"],
        ["Carbenicillin", "Penicillins", "J01CA03", "Watch", "No"],
        ["Carindacillin", "Penicillins", "J01CA05", "Watch", "No"],
        ["Carumonam", "Monobactams", "J01DF02", "Reserve", "No"],
        ["Cefacetrile", "First-generation-cephalosporins", "J01DB10", "Access", "No"],
        ["Cefaclor", "Second-generation-cephalosporins", "J01DC04", "Watch", "No"],
        ["Cefadroxil", "First-generation-cephalosporins", "J01DB05", "Access", "No"],
        ["Cefalexin", "First-generation-cephalosporins", "J01DB01", "Access", "Yes"],
        ["Cefaloridine", "First-generation-cephalosporins", "J01DB02", "Access", "No"],
        ["Cefalotin", "First-generation-cephalosporins", "J01DB03", "Access", "No"],
        ["Cefamandole", "Second-generation-cephalosporins", "J01DC03", "Watch", "No"],
        ["Cefapirin", "First-generation-cephalosporins", "J01DB08", "Access", "No"],
        ["Cefatrizine", "First-generation-cephalosporins", "J01DB07", "Access", "No"],
        ["Cefazedone", "First-generation-cephalosporins", "J01DB06", "Access", "No"],
        ["Cefazolin", "First-generation-cephalosporins", "J01DB04", "Access", "Yes"],
        ["Cefbuperazone", "Second-generation-cephalosporins", "J01DC13", "Watch", "No"],
        ["Cefcapene-pivoxil", "Third-generation-cephalosporins", "J01DD17", "Watch", "No"],
        ["Cefdinir", "Third-generation-cephalosporins", "J01DD15", "Watch", "No"],
        ["Cefditoren-pivoxil", "Third-generation-cephalosporins", "J01DD16", "Watch", "No"],
        ["Cefepime", "Fourth-generation-cephalosporins", "J01DE01", "Watch", "No"],
        ["Cefetamet-pivoxil", "Third-generation-cephalosporins", "J01DD10", "Watch", "No"],
        ["Cefiderocol", "Other-cephalosporins", "J01DI04", "Reserve", "Yes"],
        ["Cefixime", "Third-generation-cephalosporins", "J01DD08", "Watch", "Yes"],
        ["Cefmenoxime", "Third-generation-cephalosporins", "J01DD05", "Watch", "No"],
        ["Cefmetazole", "Second-generation-cephalosporins", "J01DC09", "Watch", "No"],
        ["Cefminox", "Second-generation-cephalosporins", "J01DC12", "Watch", "No"],
        ["Cefodizime", "Third-generation-cephalosporins", "J01DD09", "Watch", "No"],
        ["Cefonicid", "Second-generation-cephalosporins", "J01DC06", "Watch", "No"],
        ["Cefoperazone", "Third-generation-cephalosporins", "J01DD12", "Watch", "No"],
        ["Ceforanide", "Second-generation-cephalosporins", "J01DC11", "Watch", "No"],
        ["Cefoselis", "Fourth-generation-cephalosporins", "to be assigned", "Watch", "No"],
        ["Cefotaxime", "Third-generation-cephalosporins", "J01DD01", "Watch", "Yes"],
        ["Cefotetan", "Second-generation-cephalosporins", "J01DC05", "Watch", "No"],
        ["Cefotiam", "Second-generation-cephalosporins", "J01DC07", "Watch", "No"],
        ["Cefoxitin", "Second-generation-cephalosporins", "J01DC01", "Watch", "No"],
        ["Cefozopran", "Fourth-generation-cephalosporins", "J01DE03", "Watch", "No"],
        ["Cefpiramide", "Third-generation-cephalosporins", "J01DD11", "Watch", "No"],
        ["Cefpirome", "Fourth-generation-cephalosporins", "J01DE02", "Watch", "No"],
        ["Cefpodoxime-proxetil", "Third-generation-cephalosporins", "J01DD13", "Watch", "No"],
        ["Cefprozil", "Second-generation-cephalosporins", "J01DC10", "Watch", "No"],
        ["Cefradine", "First-generation-cephalosporins", "J01DB09", "Access", "No"],
        ["Cefroxadine", "First-generation-cephalosporins", "J01DB11", "Access", "No"],
        ["Cefsulodin", "Third-generation-cephalosporins", "J01DD03", "Watch", "No"],
        ["Ceftaroline-fosamil", "Fifth-generation cephalosporins", "J01DI02", "Reserve", "No"],
        ["Ceftazidime", "Third-generation-cephalosporins", "J01DD02", "Watch", "Yes"],
        ["Ceftazidime/avibactam", "Third-generation-cephalosporins", "J01DD52", "Reserve", "Yes"],
        ["Cefteram-pivoxil", "Third-generation-cephalosporins", "J01DD18", "Watch", "No"],
        ["Ceftezole", "First-generation-cephalosporins", "J01DB12", "Access", "No"],
        ["Ceftibuten", "Third-generation-cephalosporins", "J01DD14", "Watch", "No"],
        ["Ceftizoxime", "Third-generation-cephalosporins", "J01DD07", "Watch", "No"],
        ["Ceftobiprole-medocaril", "Fifth-generation cephalosporins", "J01DI01", "Reserve", "No"],
        ["Ceftolozane/tazobactam", "Fifth-generation cephalosporins", "J01DI54", "Reserve", "Yes"],
        ["Ceftriaxone", "Third-generation-cephalosporins", "J01DD04", "Watch", "Yes"],
        ["Cefuroxime", "Second-generation-cephalosporins", "J01DC02", "Watch", "Yes"],
        ["Chloramphenicol", "Amphenicols", "J01BA01", "Access", "Yes"],
        ["Chlortetracycline", "Tetracyclines", "J01AA03", "Watch", "No"],
        ["Cinoxacin", "Quinolones", "J01MB06", "Watch", "No"],
        ["Ciprofloxacin", "Fluoroquinolones", "J01MA02", "Watch", "Yes"],
        ["Clarithromycin", "Macrolides", "J01FA09", "Watch", "Yes"],
        ["Clindamycin", "Lincosamides", "J01FF01", "Access", "Yes"],
        ["Clofoctol", "Phenol derivatives", "J01XX03", "Watch", "No"],
        ["Clometocillin", "Penicillins", "J01CE07", "Access", "No"],
        ["Clomocycline", "Tetracyclines", "J01AA11", "Watch", "No"],
        ["Cloxacillin", "Penicillins", "J01CF02", "Access", "Yes"],
        ["Colistin_IV", "Polymyxins", "J01XB01", "Reserve", "Yes"],
        ["Colistin_oral", "Polymyxins", "A07AA10", "Reserve", "No"],
        ["Dalbavancin", "Glycopeptides", "J01XA04", "Reserve", "No"],
        ["Dalfopristin/quinupristin", "Streptogramins", "J01FG02", "Reserve", "No"],
        ["Daptomycin", "Lipopeptides", "J01XX09", "Reserve", "No"],
        ["Delafloxacin", "Fluoroquinolones", "J01MA23", "Watch", "No"],
        ["Demeclocycline", "Tetracyclines", "J01AA01", "Watch", "No"],
        ["Dibekacin", "Aminoglycosides", "J01GB09", "Watch", "No"],
        ["Dicloxacillin", "Penicillins", "J01CF01", "Access", "Yes"],
        ["Dirithromycin", "Macrolides", "J01FA13", "Watch", "No"],
        ["Doripenem", "Carbapenems", "J01DH04", "Watch", "No"],
        ["Doxycycline", "Tetracyclines", "J01AA02", "Access", "Yes"],
        ["Enoxacin", "Fluoroquinolones", "J01MA04", "Watch", "No"],
        ["Epicillin", "Penicillins", "J01CA07", "Access", "No"],
        ["Eravacycline", "Tetracyclines", "J01AA13", "Reserve", "No"],
        ["Ertapenem", "Carbapenems", "J01DH03", "Watch", "No"],
        ["Erythromycin", "Macrolides", "J01FA01", "Watch", "Yes"],
        ["Faropenem", "Penems", "J01DI03", "Reserve", "No"],
        ["Fidaxomicin", "Macrolides", "A07AA12", "Watch", "No"],
        ["Fleroxacin", "Fluoroquinolones", "J01MA08", "Watch", "No"],
        ["Flomoxef", "Second-generation-cephalosporins", "J01DC14", "Watch", "No"],
        ["Flucloxacillin", "Penicillins", "J01CF05", "Access", "Yes"],
        ["Flumequine", "Quinolones", "J01MB07", "Watch", "No"],
        ["Flurithromycin", "Macrolides", "J01FA14", "Watch", "No"],
        ["Fosfomycin_IV", "Phosphonics", "J01XX01", "Reserve", "Yes"],
        ["Fosfomycin_oral", "Phosphonics", "J01XX01", "Watch", "No"],
        ["Furazidin", "Nitrofuran derivatives", "J01XE03", "Access", "No"],
        ["Fusidic-acid", "Steroid antibacterials", "J01XC01", "Watch", "No"],
        ["Garenoxacin", "Fluoroquinolones", "J01MA19", "Watch", "No"],
        ["Gatifloxacin", "Fluoroquinolones", "J01MA16", "Watch", "No"],
        ["Gemifloxacin", "Fluoroquinolones", "J01MA15", "Watch", "No"],
        ["Gentamicin", "Aminoglycosides", "J01GB03", "Access", "Yes"],
        ["Grepafloxacin", "Fluoroquinolones", "J01MA11", "Watch", "No"],
        ["Hetacillin", "Penicillins", "J01CA18", "Access", "No"],
        ["Iclaprim", "Trimethoprim-derivatives", "J01EA03", "Reserve", "No"],
        ["Imipenem/cilastatin", "Carbapenems", "J01DH51", "Watch", "Yes"],
        ["Imipenem/cilastatin/relebactam", "Carbapenems", "J01DH56", "Reserve", "No"],
        ["Isepamicin", "Aminoglycosides", "J01GB11", "Watch", "No"],
        ["Josamycin", "Macrolides", "J01FA07", "Watch", "No"],
        ["Kanamycin_IV", "Aminoglycosides", "J01GB04", "Watch", "No"],
        ["Kanamycin_oral", "Aminoglycosides", "A07AA08", "Watch", "No"],
        ["Lascufloxacin", "Fluoroquinolones", "J01MA25", "Watch", "No"],
        ["Latamoxef", "Third-generation-cephalosporins", "J01DD06", "Watch", "No"],
        ["Lefamulin", "Pleuromutilin", "J01XX12", "Reserve", "No"],
        ["Levofloxacin", "Fluoroquinolones", "J01MA12", "Watch", "No"],
        ["Levonadifloxacin", "Fluoroquinolones", "J01MA24", "Watch", "No"],
        ["Lincomycin", "Lincosamides", "J01FF02", "Watch", "No"],
        ["Linezolid", "Oxazolidinones", "J01XX08", "Reserve", "Yes"],
        ["Lomefloxacin", "Fluoroquinolones", "J01MA07", "Watch", "No"],
        ["Loracarbef", "Second-generation-cephalosporins", "J01DC08", "Watch", "No"],
        ["Lymecycline", "Tetracyclines", "J01AA04", "Watch", "No"],
        ["Mecillinam", "Penicillins", "J01CA11", "Access", "No"],
        ["Meropenem", "Carbapenems", "J01DH02", "Watch", "Yes"],
        ["Meropenem/vaborbactam", "Carbapenems", "J01DH52", "Reserve", "Yes"],
        ["Metacycline", "Tetracyclines", "J01AA05", "Watch", "No"],
        ["Metampicillin", "Penicillins", "J01CA14", "Access", "No"],
        ["Meticillin", "Penicillins", "J01CF03", "Access", "Yes"],
        ["Metronidazole_IV", "Imidazoles", "J01XD01", "Access", "Yes"],
        ["Metronidazole_oral", "Imidazoles", "P01AB01", "Access", "Yes"],
        ["Mezlocillin", "Penicillins", "J01CA10", "Watch", "No"],
        ["Micronomicin", "Aminoglycosides", "to be assigned", "Watch", "No"],
        ["Midecamycin", "Macrolides", "J01FA03", "Watch", "No"],
        ["Minocycline_IV", "Tetracyclines", "J01AA08", "Reserve", "No"],
        ["Minocycline_oral", "Tetracyclines", "J01AA08", "Watch", "No"],
        ["Miocamycin", "Macrolides", "J01FA11", "Watch", "No"],
        ["Moxifloxacin", "Fluoroquinolones", "J01MA14", "Watch", "No"],
        ["Nafcillin", "Penicillins", "J01CF06", "Access", "Yes"],
        ["Nemonoxacin", "Quinolones", "J01MB08", "Watch", "No"],
        ["Neomycin_IV", "Aminoglycosides", "J01GB05", "Watch", "No"],
        ["Neomycin_oral", "Aminoglycosides", "A07AA01", "Watch", "No"],
        ["Netilmicin", "Aminoglycosides", "J01GB07", "Watch", "No"],
        ["Nifurtoinol", "Nitrofuran derivatives", "J01XE02", "Access", "No"],
        ["Nitrofurantoin", "Nitrofuran-derivatives", "J01XE01", "Access", "Yes"],
        ["Norfloxacin", "Fluoroquinolones", "J01MA06", "Watch", "No"],
        ["Ofloxacin", "Fluoroquinolones", "J01MA01", "Watch", "No"],
        ["Oleandomycin", "Macrolides", "J01FA05", "Watch", "No"],
        ["Omadacycline", "Tetracyclines", "J01AA15", "Reserve", "No"],
        ["Oritavancin", "Glycopeptides", "J01XA05", "Reserve", "No"],
        ["Ornidazole_IV", "Imidazoles", "J01XD03", "Access", "No"],
        ["Ornidazole_oral", "Imidazoles", "P01AB03", "Access", "No"],
        ["Oxacillin", "Penicillins", "J01CF04", "Access", "Yes"],
        ["Oxolinic-acid", "Quinolones", "J01MB05", "Watch", "No"],
        ["Oxytetracycline", "Tetracyclines", "J01AA06", "Watch", "No"],
        ["Panipenem", "Carbapenems", "J01DH55", "Watch", "No"],
        ["Pazufloxacin", "Fluoroquinolones", "J01MA18", "Watch", "No"],
        ["Pefloxacin", "Fluoroquinolones", "J01MA03", "Watch", "No"],
        ["Penamecillin", "Penicillins", "J01CE06", "Access", "No"],
        ["Penimepicycline", "Tetracyclines", "J01AA10", "Watch", "No"],
        ["Pheneticillin", "Penicillins", "J01CE05", "Watch", "No"],
        ["Phenoxymethylpenicillin", "Penicillins", "J01CE02", "Access", "Yes"],
        ["Pipemidic-acid", "Quinolones", "J01MB04", "Watch", "No"],
        ["Piperacillin", "Penicillins", "J01CA12", "Watch", "No"],
        ["Piperacillin/tazobactam", "Beta-lactam/beta-lactamase-inhibitor_anti-pseudomonal", "J01CR05", "Watch", "Yes"],
        ["Piromidic-acid", "Quinolones", "J01MB03", "Watch", "No"],
        ["Pivampicillin", "Penicillins", "J01CA02", "Access", "No"],
        ["Pivmecillinam", "Penicillins", "J01CA08", "Access", "No"],
        ["Plazomicin", "Aminoglycosides", "J01GB14", "Reserve", "Yes"],
        ["Polymyxin-B_IV", "Polymyxins", "J01XB02", "Reserve", "Yes"],
        ["Polymyxin-B_oral", "Polymyxins", "A07AA05", "Reserve", "No"],
        ["Pristinamycin", "Streptogramins", "J01FG01", "Watch", "No"],
        ["Procaine-benzylpenicillin", "Penicillins", "J01CE09", "Access", "Yes"],
        ["Propicillin", "Penicillins", "J01CE03", "Access", "No"],
        ["Prulifloxacin", "Fluoroquinolones", "J01MA17", "Watch", "No"],
        ["Ribostamycin", "Aminoglycosides", "J01GB10", "Watch", "No"],
        ["Rifabutin", "Rifamycins", "J04AB04", "Watch", "No"],
        ["Rifampicin", "Rifamycins", "J04AB02", "Watch", "No"],
        ["Rifamycin_IV", "Rifamycins", "J04AB03", "Watch", "No"],
        ["Rifamycin_oral", "Rifamycins", "A07AA13", "Watch", "No"],
        ["Rifaximin", "Rifamycins", "A07AA11", "Watch", "No"],
        ["Rokitamycin", "Macrolides", "J01FA12", "Watch", "No"],
        ["Rolitetracycline", "Tetracyclines", "J01AA09", "Watch", "No"],
        ["Rosoxacin", "Quinolones", "J01MB01", "Watch", "No"],
        ["Roxithromycin", "Macrolides", "J01FA06", "Watch", "No"],
        ["Rufloxacin", "Fluoroquinolones", "J01MA10", "Watch", "No"],
        ["Sarecycline", "Tetracyclines", "J01AA14", "Watch", "No"],
        ["Secnidazole", "Imidazoles", "P01AB07", "Access", "No"],
        ["Sisomicin", "Aminoglycosides", "J01GB08", "Watch", "No"],
        ["Sitafloxacin", "Fluoroquinolones", "J01MA21", "Watch", "No"],
        ["Solithromycin", "Macrolides", "J01FA16", "Watch", "No"],
        ["Sparfloxacin", "Fluoroquinolones", "J01MA09", "Watch", "No"],
        ["Spectinomycin", "Aminocyclitols", "J01XX04", "Access", "Yes"],
        ["Spiramycin", "Macrolides", "J01FA02", "Watch", "No"],
        ["Streptoduocin", "Aminoglycosides", "J01GA02", "Watch", "No"],
        ["Streptomycin_IV", "Aminoglycosides", "J01GA01", "Watch", "No"],
        ["Streptomycin_oral", "Aminoglycosides", "A07AA04", "Watch", "No"],
        ["Sulbactam", "Beta-lactamase-inhibitors", "J01CG01", "Access", "No"],
        ["Sulbenicillin", "Penicillins", "J01CA16", "Watch", "No"],
        ["Sulfadiazine", "Sulfonamides", "J01EC02", "Access", "No"],
        ["Sulfadiazine/tetroxoprim", "Sulfonamide-trimethoprim-combinations", "J01EE06", "Access", "No"],
        ["Sulfadiazine/trimethoprim", "Sulfonamide-trimethoprim-combinations", "J01EE02", "Access", "No"],
        ["Sulfadimethoxine", "Sulfonamides", "J01ED01", "Access", "No"],
        ["Sulfadimidine", "Sulfonamides", "J01EB03", "Access", "No"],
        ["Sulfadimidine/trimethoprim", "Sulfonamide-trimethoprim-combinations", "J01EE05", "Access", "No"],
        ["Sulfafurazole", "Sulfonamides", "J01EB05", "Access", "No"],
        ["Sulfaisodimidine", "Sulfonamides", "J01EB01", "Access", "No"],
        ["Sulfalene", "Sulfonamides", "J01ED02", "Access", "No"],
        ["Sulfamazone", "Sulfonamides", "J01ED09", "Access", "No"],
        ["Sulfamerazine", "Sulfonamides", "J01ED07", "Access", "No"],
        ["Sulfamerazine/trimethoprim", "Sulfonamide-trimethoprim-combinations", "J01EE07", "Access", "No"],
        ["Sulfamethizole", "Sulfonamides", "J01EB02", "Access", "No"],
        ["Sulfamethoxazole", "Sulfonamides", "J01EC01", "Access", "No"],
        ["Sulfamethoxazole/trimethoprim", "Sulfonamide-trimethoprim-combinations", "J01EE01", "Access", "Yes"],
        ["Sulfamethoxypyridazine", "Sulfonamides", "J01ED05", "Access", "No"],
        ["Sulfametomidine", "Sulfonamides", "J01ED03", "Access", "No"],
        ["Sulfametoxydiazine", "Sulfonamides", "J01ED04", "Access", "No"],
        ["Sulfametrole/trimethoprim", "Sulfonamide-trimethoprim-combinations", "J01EE03", "Access", "No"],
        ["Sulfamoxole", "Sulfonamides", "J01EC03", "Access", "No"],
        ["Sulfamoxole/trimethoprim", "Sulfonamide-trimethoprim-combinations", "J01EE04", "Access", "No"],
        ["Sulfanilamide", "Sulfonamides", "J01EB06", "Access", "No"],
        ["Sulfaperin", "Sulfonamides", "J01ED06", "Access", "No"],
        ["Sulfaphenazole", "Sulfonamides", "J01ED08", "Access", "No"],
        ["Sulfapyridine", "Sulfonamides", "J01EB04", "Access", "No"],
        ["Sulfathiazole", "Sulfonamides", "J01EB07", "Access", "No"],
        ["Sulfathiourea", "Sulfonamides", "J01EB08", "Access", "No"],
        ["Sultamicillin", "Beta-lactam/beta-lactamase-inhibitor", "J01CR04", "Access", "No"],
        ["Talampicillin", "Penicillins", "J01CA15", "Access", "No"],
        ["Tazobactam", "Beta-lactamase-inhibitors", "J01CG02", "Watch", "No"],
        ["Tebipenem", "Carbapenems", "J01DH06", "Watch", "No"],
        ["Tedizolid", "Oxazolidinones", "J01XX11", "Reserve", "Yes"],
        ["Teicoplanin", "Glycopeptides", "J01XA02", "Watch", "No"],
        ["Telavancin", "Glycopeptides", "J01XA03", "Reserve", "No"],
        ["Telithromycin", "Macrolides", "J01FA15", "Watch", "No"],
        ["Temafloxacin", "Fluoroquinolones", "J01MA05", "Watch", "No"],
        ["Temocillin", "Penicillins", "J01CA17", "Watch", "No"],
        ["Tetracycline", "Tetracyclines", "J01AA07", "Access", "No"],
        ["Thiamphenicol", "Amphenicols", "J01BA02", "Access", "No"],
        ["Ticarcillin", "Penicillins", "J01CA13", "Watch", "No"],
        ["Tigecycline", "Glycylcyclines", "J01AA12", "Reserve", "No"],
        ["Tinidazole_IV", "Imidazoles", "J01XD02", "Access", "No"],
        ["Tinidazole_oral", "Imidazoles", "P01AB02", "Access", "No"],
        ["Tobramycin", "Aminoglycosides", "J01GB01", "Watch", "No"],
        ["Tosufloxacin", "Fluoroquinolones", "J01MA22", "Watch", "No"],
        ["Trimethoprim", "Trimethoprim-derivatives", "J01EA01", "Access", "Yes"],
        ["Troleandomycin", "Macrolides", "J01FA08", "Watch", "No"],
        ["Trovafloxacin", "Fluoroquinolones", "J01MA13", "Watch", "No"],
        ["Vancomycin_IV", "Glycopeptides", "J01XA01", "Watch", "Yes"],
        ["Vancomycin_oral", "Glycopeptides", "A07AA09", "Watch", "Yes"],
    ]

    # Create DataFrame
    df = pd.DataFrame(data, columns=['Antibiotic', 'Class', 'ATC', 'Category', 'EML'])
    return df


# Load the drug database
drug_db = create_drug_database()

# Get list of all drug names for the selectbox
all_drug_names = sorted(drug_db['Antibiotic'].tolist())

# Create tabs for different input methods
tab1, tab2 = st.tabs(["Drug Selector", "Database View"])

with tab1:
    st.header("Select Drugs for Classification")

    # Multi-select dropdown for drug selection
    selected_drugs = st.multiselect(
        "Select drugs to classify:",
        options=all_drug_names,
        default=None,
        help="Select one or more drugs from the list"
    )

    # Display selected drugs count
    if selected_drugs:
        st.subheader(f"Selected {len(selected_drugs)} Drug(s)")

        # Display selected drugs in a compact format
        cols = st.columns(4)
        for i, drug in enumerate(selected_drugs):
            with cols[i % 4]:
                # Get drug info
                drug_info = drug_db[drug_db['Antibiotic'] == drug]
                if not drug_info.empty:
                    category = drug_info.iloc[0]['Category']
                    # Color indicators
                    if category == 'Access':
                        color_indicator = "🟢"
                    elif category == 'Watch':
                        color_indicator = "🟡"
                    else:
                        color_indicator = "🔴"

                    st.markdown(f"**{color_indicator} {drug}**")

    # Classify button
    if selected_drugs:
        col1, col2 = st.columns([1, 3])
        with col1:
            classify_button = st.button("Classify Selected Drugs", use_container_width=True, type="primary")

        if classify_button:
            # Get classification for selected drugs
            results = drug_db[drug_db['Antibiotic'].isin(selected_drugs)]

            if not results.empty:
                st.success(f"Classified {len(results)} drug(s)")

                # Display results with high contrast colors
                for _, row in results.iterrows():
                    # High contrast colors - brighter for better visibility
                    if row['Category'] == 'Access':
                        color = "🟢"
                        bg_color = "#66BB6A"  # Brighter green
                        text_color = "#1B5E20"  # Dark green
                        border_color = "#2E7D32"
                    elif row['Category'] == 'Watch':
                        color = "🟡"
                        bg_color = "#FFD54F"  # Brighter yellow
                        text_color = "#5D4037"  # Dark brown
                        border_color = "#FF8F00"
                    else:  # Reserve
                        color = "🔴"
                        bg_color = "#EF5350"  # Brighter red
                        text_color = "#B71C1C"  # Dark red
                        border_color = "#D32F2F"

                    # Create a styled card with high contrast
                    st.markdown(f"""
                    <div style="
                        background-color: {bg_color};
                        padding: 15px;
                        border-radius: 10px;
                        border-left: 5px solid {border_color};
                        margin: 10px 0;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    ">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h4 style="color: {text_color}; margin: 0; font-weight: bold; font-size: 1.2em;">{row['Antibiotic']}</h4>
                                <p style="margin: 5px 0; color: {text_color}; font-size: 1.1em;"><strong>{color} {row['Category']}</strong></p>
                            </div>
                            <div style="text-align: right;">
                                <p style="margin: 5px 0; color: {text_color};"><strong>Class:</strong> {row['Class']}</p>
                                <p style="margin: 5px 0; color: {text_color};"><strong>EML:</strong> {"🟢 Yes" if row['EML'] == "Yes" else "🔴 No"}</p>
                            </div>
                        </div>
                        <div style="margin-top: 10px; padding-top: 10px; border-top: 2px solid {border_color};">
                            <p style="margin: 0; color: {text_color}; font-weight: bold;"><strong>ATC Code:</strong> {row['ATC']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Download results
                csv = results.to_csv(index=False)
                st.download_button(
                    label="Download Results as CSV",
                    data=csv,
                    file_name="aware_classification_results.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.warning("No classification data found for selected drugs.")
    else:
        st.info("Select drugs from the list above to see their classification.")

with tab2:
    st.header("Complete Drug Database")

    st.markdown("""
    Browse the complete database of antibiotics with their AWaRe classifications.
    Use the filters below to search for specific drugs or filter by category.
    """)

    # Add filters
    col1, col2, col3 = st.columns(3)

    with col1:
        category_filter = st.multiselect(
            "Filter by AWaRe Category:",
            options=["Access", "Watch", "Reserve"],
            default=None
        )

    with col2:
        eml_filter = st.multiselect(
            "Filter by EML Status:",
            options=["Yes", "No"],
            default=None
        )

    with col3:
        search_db = st.text_input("Search drugs:", placeholder="Type to search...")

    # Apply filters
    filtered_db = drug_db.copy()

    if category_filter:
        filtered_db = filtered_db[filtered_db['Category'].isin(category_filter)]

    if eml_filter:
        filtered_db = filtered_db[filtered_db['EML'].isin(eml_filter)]

    if search_db:
        search_lower = search_db.lower()
        filtered_db = filtered_db[
            filtered_db['Antibiotic'].str.lower().str.contains(search_lower) |
            filtered_db['Class'].str.lower().str.contains(search_lower) |
            filtered_db['ATC'].str.lower().str.contains(search_lower)
            ]

    # Display the database with high contrast colors
    st.subheader(f"Showing {len(filtered_db)} of {len(drug_db)} drugs")


    # High contrast color mapping function
    def highlight_rows_high_contrast(row):
        if row['Category'] == 'Access':
            # Bright green background with dark green text
            return ['background-color: #66BB6A; color: #1B5E20; font-weight: bold'] * len(row)
        elif row['Category'] == 'Watch':
            # Bright yellow background with dark brown text
            return ['background-color: #FFD54F; color: #5D4037; font-weight: bold'] * len(row)
        else:  # Reserve
            # Bright red background with dark red text
            return ['background-color: #EF5350; color: #B71C1C; font-weight: bold'] * len(row)


    # Apply high contrast styling
    styled_db = filtered_db.style.apply(highlight_rows_high_contrast, axis=1)

    # Display the database
    st.dataframe(
        styled_db,
        use_container_width=True,
        column_config={
            "Antibiotic": st.column_config.TextColumn(
                "Drug Name",
                help="Name of the antibiotic"
            ),
            "Category": st.column_config.TextColumn(
                "AWaRe Category",
                help="AWaRe classification category"
            ),
            "Class": st.column_config.TextColumn(
                "Drug Class",
                help="Pharmacological class of the antibiotic"
            ),
            "ATC": st.column_config.TextColumn(
                "ATC Code",
                help="Anatomical Therapeutic Chemical code"
            ),
            "EML": st.column_config.TextColumn(
                "EML Status",
                help="Included in WHO Essential Medicines List"
            )
        },
        hide_index=True
    )

    # Database statistics with high contrast
    st.subheader("Database Statistics")

    total_drugs = len(drug_db)
    access_count = len(drug_db[drug_db['Category'] == 'Access'])
    watch_count = len(drug_db[drug_db['Category'] == 'Watch'])
    reserve_count = len(drug_db[drug_db['Category'] == 'Reserve'])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #333;">
            <h3 style="margin: 0; color: #333;">Total Drugs</h3>
            <h2 style="margin: 5px 0; color: #333;">{total_drugs}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background-color: #66BB6A; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #1B5E20;">
            <h3 style="margin: 0; color: white;">Access</h3>
            <h2 style="margin: 5px 0; color: white;">{access_count}</h2>
            <p style="margin: 0; color: white; font-weight: bold;">{(access_count / total_drugs * 100):.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="background-color: #FFD54F; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #FF8F00;">
            <h3 style="margin: 0; color: #5D4037;">Watch</h3>
            <h2 style="margin: 5px 0; color: #5D4037;">{watch_count}</h2>
            <p style="margin: 0; color: #5D4037; font-weight: bold;">{(watch_count / total_drugs * 100):.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div style="background-color: #EF5350; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #D32F2F;">
            <h3 style="margin: 0; color: white;">Reserve</h3>
            <h2 style="margin: 5px 0; color: white;">{reserve_count}</h2>
            <p style="margin: 0; color: white; font-weight: bold;">{(reserve_count / total_drugs * 100):.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em;">
    <p><strong>WHO AWaRe Antibiotic Classification Tool</strong></p>
    <p>Based on WHO Access, Watch, Reserve (AWaRe) classification of antibiotics for evaluation and monitoring of use, 2023</p>
    <p>For informational purposes only. Consult official guidelines for clinical decisions.</p>
</div>
""", unsafe_allow_html=True)