import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# Set up the page
st.set_page_config(
    page_title="WHO AWaRe Drug Classifier",
    page_icon="💊",
    layout="wide"
)

# Title and description
st.title("💊 WHO AWaRe Antibiotic Classification")
st.markdown("""
This app classifies antibiotics into the WHO AWaRe categories (Access, Watch, Reserve) based on the 2023 WHO classification.
Upload a list of drug names or enter them manually to get their classification.
""")

# Sidebar for information
with st.sidebar:
    st.header("About AWaRe Classification")
    st.markdown("""
    **AWaRe Categories:**
    - **Access**: First or second choice empiric treatment options
    - **Watch**: Higher resistance potential, key stewardship targets
    - **Reserve**: "Last resort" for multidrug-resistant infections

    **EML Status:**
    - **Yes**: Included in WHO Essential Medicines List
    - **No**: Not included in WHO Essential Medicines List

    *Source: WHO Access, Watch, Reserve (AWaRe) classification 2023*
    """)

    st.divider()
    st.caption("Developed using WHO drug classification data")


# Since we can't directly access the file, I'll create a function to parse the provided data
def create_drug_database_from_text():
    """Create drug database from the provided Excel text content"""

    # Parse the text data from the Excel file you provided
    # This is a manual parsing of the AWaRe classification 2023 sheet
    data_lines = """
Amikacin,Aminoglycosides,J01GB06,Access,Yes
Amoxicillin,Penicillins,J01CA04,Access,Yes
Amoxicillin/clavulanic-acid,Beta-lactam/beta-lactamase-inhibitor,J01CR02,Access,Yes
Ampicillin,Penicillins,J01CA01,Access,Yes
Ampicillin/sulbactam,Beta-lactam/beta-lactamase-inhibitor,J01CR01,Access,No
Arbekacin,Aminoglycosides,J01GB12,Watch,No
Aspoxicillin,Penicillins,J01CA19,Watch,No
Azidocillin,Penicillins,J01CE04,Access,No
Azithromycin,Macrolides,J01FA10,Watch,Yes
Azlocillin,Penicillins,J01CA09,Watch,No
Aztreonam,Monobactams,J01DF01,Reserve,No
Bacampicillin,Penicillins,J01CA06,Access,No
Bekanamycin,Aminoglycosides,J01GB13,Watch,No
Benzathine-benzylpenicillin,Penicillins,J01CE08,Access,Yes
Benzylpenicillin,Penicillins,J01CE01,Access,Yes
Biapenem,Carbapenems,J01DH05,Watch,No
Brodimoprim,Trimethoprim-derivatives,J01EA02,Access,No
Carbenicillin,Penicillins,J01CA03,Watch,No
Carindacillin,Penicillins,J01CA05,Watch,No
Carumonam,Monobactams,J01DF02,Reserve,No
Cefacetrile,First-generation-cephalosporins,J01DB10,Access,No
Cefaclor,Second-generation-cephalosporins,J01DC04,Watch,No
Cefadroxil,First-generation-cephalosporins,J01DB05,Access,No
Cefalexin,First-generation-cephalosporins,J01DB01,Access,Yes
Cefaloridine,First-generation-cephalosporins,J01DB02,Access,No
Cefalotin,First-generation-cephalosporins,J01DB03,Access,No
Cefamandole,Second-generation-cephalosporins,J01DC03,Watch,No
Cefapirin,First-generation-cephalosporins,J01DB08,Access,No
Cefatrizine,First-generation-cephalosporins,J01DB07,Access,No
Cefazedone,First-generation-cephalosporins,J01DB06,Access,No
Cefazolin,First-generation-cephalosporins,J01DB04,Access,Yes
Cefbuperazone,Second-generation-cephalosporins,J01DC13,Watch,No
Cefcapene-pivoxil,Third-generation-cephalosporins,J01DD17,Watch,No
Cefdinir,Third-generation-cephalosporins,J01DD15,Watch,No
Cefditoren-pivoxil,Third-generation-cephalosporins,J01DD16,Watch,No
Cefepime,Fourth-generation-cephalosporins,J01DE01,Watch,No
Cefetamet-pivoxil,Third-generation-cephalosporins,J01DD10,Watch,No
Cefiderocol,Other-cephalosporins,J01DI04,Reserve,Yes
Cefixime,Third-generation-cephalosporins,J01DD08,Watch,Yes
Cefmenoxime,Third-generation-cephalosporins,J01DD05,Watch,No
Cefmetazole,Second-generation-cephalosporins,J01DC09,Watch,No
Cefminox,Second-generation-cephalosporins,J01DC12,Watch,No
Cefodizime,Third-generation-cephalosporins,J01DD09,Watch,No
Cefonicid,Second-generation-cephalosporins,J01DC06,Watch,No
Cefoperazone,Third-generation-cephalosporins,J01DD12,Watch,No
Ceforanide,Second-generation-cephalosporins,J01DC11,Watch,No
Cefoselis,Fourth-generation-cephalosporins,to be assigned,Watch,No
Cefotaxime,Third-generation-cephalosporins,J01DD01,Watch,Yes
Cefotetan,Second-generation-cephalosporins,J01DC05,Watch,No
Cefotiam,Second-generation-cephalosporins,J01DC07,Watch,No
Cefoxitin,Second-generation-cephalosporins,J01DC01,Watch,No
Cefozopran,Fourth-generation-cephalosporins,J01DE03,Watch,No
Cefpiramide,Third-generation-cephalosporins,J01DD11,Watch,No
Cefpirome,Fourth-generation-cephalosporins,J01DE02,Watch,No
Cefpodoxime-proxetil,Third-generation-cephalosporins,J01DD13,Watch,No
Cefprozil,Second-generation-cephalosporins,J01DC10,Watch,No
Cefradine,First-generation-cephalosporins,J01DB09,Access,No
Cefroxadine,First-generation-cephalosporins,J01DB11,Access,No
Cefsulodin,Third-generation-cephalosporins,J01DD03,Watch,No
Ceftaroline-fosamil,Fifth-generation cephalosporins,J01DI02,Reserve,No
Ceftazidime,Third-generation-cephalosporins,J01DD02,Watch,Yes
Ceftazidime/avibactam,Third-generation-cephalosporins,J01DD52,Reserve,Yes
Cefteram-pivoxil,Third-generation-cephalosporins,J01DD18,Watch,No
Ceftezole,First-generation-cephalosporins,J01DB12,Access,No
Ceftibuten,Third-generation-cephalosporins,J01DD14,Watch,No
Ceftizoxime,Third-generation-cephalosporins,J01DD07,Watch,No
Ceftobiprole-medocaril,Fifth-generation cephalosporins,J01DI01,Reserve,No
Ceftolozane/tazobactam,Fifth-generation cephalosporins,J01DI54,Reserve,Yes
Ceftriaxone,Third-generation-cephalosporins,J01DD04,Watch,Yes
Cefuroxime,Second-generation-cephalosporins,J01DC02,Watch,Yes
Chloramphenicol,Amphenicols,J01BA01,Access,Yes
Chlortetracycline,Tetracyclines,J01AA03,Watch,No
Cinoxacin,Quinolones,J01MB06,Watch,No
Ciprofloxacin,Fluoroquinolones,J01MA02,Watch,Yes
Clarithromycin,Macrolides,J01FA09,Watch,Yes
Clindamycin,Lincosamides,J01FF01,Access,Yes
Clofoctol,Phenol derivatives,J01XX03,Watch,No
Clometocillin,Penicillins,J01CE07,Access,No
Clomocycline,Tetracyclines,J01AA11,Watch,No
Cloxacillin,Penicillins,J01CF02,Access,Yes
Colistin_IV,Polymyxins,J01XB01,Reserve,Yes
Colistin_oral,Polymyxins,A07AA10,Reserve,No
Dalbavancin,Glycopeptides,J01XA04,Reserve,No
Dalfopristin/quinupristin,Streptogramins,J01FG02,Reserve,No
Daptomycin,Lipopeptides,J01XX09,Reserve,No
Delafloxacin,Fluoroquinolones,J01MA23,Watch,No
Demeclocycline,Tetracyclines,J01AA01,Watch,No
Dibekacin,Aminoglycosides,J01GB09,Watch,No
Dicloxacillin,Penicillins,J01CF01,Access,Yes
Dirithromycin,Macrolides,J01FA13,Watch,No
Doripenem,Carbapenems,J01DH04,Watch,No
Doxycycline,Tetracyclines,J01AA02,Access,Yes
Enoxacin,Fluoroquinolones,J01MA04,Watch,No
Epicillin,Penicillins,J01CA07,Access,No
Eravacycline,Tetracyclines,J01AA13,Reserve,No
Ertapenem,Carbapenems,J01DH03,Watch,No
Erythromycin,Macrolides,J01FA01,Watch,Yes
Faropenem,Penems,J01DI03,Reserve,No
Fidaxomicin,Macrolides,A07AA12,Watch,No
Fleroxacin,Fluoroquinolones,J01MA08,Watch,No
Flomoxef,Second-generation-cephalosporins,J01DC14,Watch,No
Flucloxacillin,Penicillins,J01CF05,Access,Yes
Flumequine,Quinolones,J01MB07,Watch,No
Flurithromycin,Macrolides,J01FA14,Watch,No
Fosfomycin_IV,Phosphonics,J01XX01,Reserve,Yes
Fosfomycin_oral,Phosphonics,J01XX01,Watch,No
Furazidin,Nitrofuran derivatives,J01XE03,Access,No
Fusidic-acid,Steroid antibacterials,J01XC01,Watch,No
Garenoxacin,Fluoroquinolones,J01MA19,Watch,No
Gatifloxacin,Fluoroquinolones,J01MA16,Watch,No
Gemifloxacin,Fluoroquinolones,J01MA15,Watch,No
Gentamicin,Aminoglycosides,J01GB03,Access,Yes
Grepafloxacin,Fluoroquinolones,J01MA11,Watch,No
Hetacillin,Penicillins,J01CA18,Access,No
Iclaprim,Trimethoprim-derivatives,J01EA03,Reserve,No
Imipenem/cilastatin,Carbapenems,J01DH51,Watch,Yes
Imipenem/cilastatin/relebactam,Carbapenems,J01DH56,Reserve,No
Isepamicin,Aminoglycosides,J01GB11,Watch,No
Josamycin,Macrolides,J01FA07,Watch,No
Kanamycin_IV,Aminoglycosides,J01GB04,Watch,No
Kanamycin_oral,Aminoglycosides,A07AA08,Watch,No
Lascufloxacin,Fluoroquinolones,J01MA25,Watch,No
Latamoxef,Third-generation-cephalosporins,J01DD06,Watch,No
Lefamulin,Pleuromutilin,J01XX12,Reserve,No
Levofloxacin,Fluoroquinolones,J01MA12,Watch,No
Levonadifloxacin,Fluoroquinolones,J01MA24,Watch,No
Lincomycin,Lincosamides,J01FF02,Watch,No
Linezolid,Oxazolidinones,J01XX08,Reserve,Yes
Lomefloxacin,Fluoroquinolones,J01MA07,Watch,No
Loracarbef,Second-generation-cephalosporins,J01DC08,Watch,No
Lymecycline,Tetracyclines,J01AA04,Watch,No
Mecillinam,Penicillins,J01CA11,Access,No
Meropenem,Carbapenems,J01DH02,Watch,Yes
Meropenem/vaborbactam,Carbapenems,J01DH52,Reserve,Yes
Metacycline,Tetracyclines,J01AA05,Watch,No
Metampicillin,Penicillins,J01CA14,Access,No
Meticillin,Penicillins,J01CF03,Access,Yes
Metronidazole_IV,Imidazoles,J01XD01,Access,Yes
Metronidazole_oral,Imidazoles,P01AB01,Access,Yes
Mezlocillin,Penicillins,J01CA10,Watch,No
Micronomicin,Aminoglycosides,to be assigned,Watch,No
Midecamycin,Macrolides,J01FA03,Watch,No
Minocycline_IV,Tetracyclines,J01AA08,Reserve,No
Minocycline_oral,Tetracyclines,J01AA08,Watch,No
Miocamycin,Macrolides,J01FA11,Watch,No
Moxifloxacin,Fluoroquinolones,J01MA14,Watch,No
Nafcillin,Penicillins,J01CF06,Access,Yes
Nemonoxacin,Quinolones,J01MB08,Watch,No
Neomycin_IV,Aminoglycosides,J01GB05,Watch,No
Neomycin_oral,Aminoglycosides,A07AA01,Watch,No
Netilmicin,Aminoglycosides,J01GB07,Watch,No
Nifurtoinol,Nitrofuran derivatives,J01XE02,Access,No
Nitrofurantoin,Nitrofuran-derivatives,J01XE01,Access,Yes
Norfloxacin,Fluoroquinolones,J01MA06,Watch,No
Ofloxacin,Fluoroquinolones,J01MA01,Watch,No
Oleandomycin,Macrolides,J01FA05,Watch,No
Omadacycline,Tetracyclines,J01AA15,Reserve,No
Oritavancin,Glycopeptides,J01XA05,Reserve,No
Ornidazole_IV,Imidazoles,J01XD03,Access,No
Ornidazole_oral,Imidazoles,P01AB03,Access,No
Oxacillin,Penicillins,J01CF04,Access,Yes
Oxolinic-acid,Quinolones,J01MB05,Watch,No
Oxytetracycline,Tetracyclines,J01AA06,Watch,No
Panipenem,Carbapenems,J01DH55,Watch,No
Pazufloxacin,Fluoroquinolones,J01MA18,Watch,No
Pefloxacin,Fluoroquinolones,J01MA03,Watch,No
Penamecillin,Penicillins,J01CE06,Access,No
Penimepicycline,Tetracyclines,J01AA10,Watch,No
Pheneticillin,Penicillins,J01CE05,Watch,No
Phenoxymethylpenicillin,Penicillins,J01CE02,Access,Yes
Pipemidic-acid,Quinolones,J01MB04,Watch,No
Piperacillin,Penicillins,J01CA12,Watch,No
Piperacillin/tazobactam,Beta-lactam/beta-lactamase-inhibitor_anti-pseudomonal,J01CR05,Watch,Yes
Piromidic-acid,Quinolones,J01MB03,Watch,No
Pivampicillin,Penicillins,J01CA02,Access,No
Pivmecillinam,Penicillins,J01CA08,Access,No
Plazomicin,Aminoglycosides,J01GB14,Reserve,Yes
Polymyxin-B_IV,Polymyxins,J01XB02,Reserve,Yes
Polymyxin-B_oral,Polymyxins,A07AA05,Reserve,No
Pristinamycin,Streptogramins,J01FG01,Watch,No
Procaine-benzylpenicillin,Penicillins,J01CE09,Access,Yes
Propicillin,Penicillins,J01CE03,Access,No
Prulifloxacin,Fluoroquinolones,J01MA17,Watch,No
Ribostamycin,Aminoglycosides,J01GB10,Watch,No
Rifabutin,Rifamycins,J04AB04,Watch,No
Rifampicin,Rifamycins,J04AB02,Watch,No
Rifamycin_IV,Rifamycins,J04AB03,Watch,No
Rifamycin_oral,Rifamycins,A07AA13,Watch,No
Rifaximin,Rifamycins,A07AA11,Watch,No
Rokitamycin,Macrolides,J01FA12,Watch,No
Rolitetracycline,Tetracyclines,J01AA09,Watch,No
Rosoxacin,Quinolones,J01MB01,Watch,No
Roxithromycin,Macrolides,J01FA06,Watch,No
Rufloxacin,Fluoroquinolones,J01MA10,Watch,No
Sarecycline,Tetracyclines,J01AA14,Watch,No
Secnidazole,Imidazoles,P01AB07,Access,No
Sisomicin,Aminoglycosides,J01GB08,Watch,No
Sitafloxacin,Fluoroquinolones,J01MA21,Watch,No
Solithromycin,Macrolides,J01FA16,Watch,No
Sparfloxacin,Fluoroquinolones,J01MA09,Watch,No
Spectinomycin,Aminocyclitols,J01XX04,Access,Yes
Spiramycin,Macrolides,J01FA02,Watch,No
Streptoduocin,Aminoglycosides,J01GA02,Watch,No
Streptomycin_IV,Aminoglycosides,J01GA01,Watch,No
Streptomycin_oral,Aminoglycosides,A07AA04,Watch,No
Sulbactam,Beta-lactamase-inhibitors,J01CG01,Access,No
Sulbenicillin,Penicillins,J01CA16,Watch,No
Sulfadiazine,Sulfonamides,J01EC02,Access,No
Sulfadiazine/tetroxoprim,Sulfonamide-trimethoprim-combinations,J01EE06,Access,No
Sulfadiazine/trimethoprim,Sulfonamide-trimethoprim-combinations,J01EE02,Access,No
Sulfadimethoxine,Sulfonamides,J01ED01,Access,No
Sulfadimidine,Sulfonamides,J01EB03,Access,No
Sulfadimidine/trimethoprim,Sulfonamide-trimethoprim-combinations,J01EE05,Access,No
Sulfafurazole,Sulfonamides,J01EB05,Access,No
Sulfaisodimidine,Sulfonamides,J01EB01,Access,No
Sulfalene,Sulfonamides,J01ED02,Access,No
Sulfamazone,Sulfonamides,J01ED09,Access,No
Sulfamerazine,Sulfonamides,J01ED07,Access,No
Sulfamerazine/trimethoprim,Sulfonamide-trimethoprim-combinations,J01EE07,Access,No
Sulfamethizole,Sulfonamides,J01EB02,Access,No
Sulfamethoxazole,Sulfonamides,J01EC01,Access,No
Sulfamethoxazole/trimethoprim,Sulfonamide-trimethoprim-combinations,J01EE01,Access,Yes
Sulfamethoxypyridazine,Sulfonamides,J01ED05,Access,No
Sulfametomidine,Sulfonamides,J01ED03,Access,No
Sulfametoxydiazine,Sulfonamides,J01ED04,Access,No
Sulfametrole/trimethoprim,Sulfonamide-trimethoprim-combinations,J01EE03,Access,No
Sulfamoxole,Sulfonamides,J01EC03,Access,No
Sulfamoxole/trimethoprim,Sulfonamide-trimethoprim-combinations,J01EE04,Access,No
Sulfanilamide,Sulfonamides,J01EB06,Access,No
Sulfaperin,Sulfonamides,J01ED06,Access,No
Sulfaphenazole,Sulfonamides,J01ED08,Access,No
Sulfapyridine,Sulfonamides,J01EB04,Access,No
Sulfathiazole,Sulfonamides,J01EB07,Access,No
Sulfathiourea,Sulfonamides,J01EB08,Access,No
Sultamicillin,Beta-lactam/beta-lactamase-inhibitor,J01CR04,Access,No
Talampicillin,Penicillins,J01CA15,Access,No
Tazobactam,Beta-lactamase-inhibitors,J01CG02,Watch,No
Tebipenem,Carbapenems,J01DH06,Watch,No
Tedizolid,Oxazolidinones,J01XX11,Reserve,Yes
Teicoplanin,Glycopeptides,J01XA02,Watch,No
Telavancin,Glycopeptides,J01XA03,Reserve,No
Telithromycin,Macrolides,J01FA15,Watch,No
Temafloxacin,Fluoroquinolones,J01MA05,Watch,No
Temocillin,Penicillins,J01CA17,Watch,No
Tetracycline,Tetracyclines,J01AA07,Access,No
Thiamphenicol,Amphenicols,J01BA02,Access,No
Ticarcillin,Penicillins,J01CA13,Watch,No
Tigecycline,Glycylcyclines,J01AA12,Reserve,No
Tinidazole_IV,Imidazoles,J01XD02,Access,No
Tinidazole_oral,Imidazoles,P01AB02,Access,No
Tobramycin,Aminoglycosides,J01GB01,Watch,No
Tosufloxacin,Fluoroquinolones,J01MA22,Watch,No
Trimethoprim,Trimethoprim-derivatives,J01EA01,Access,Yes
Troleandomycin,Macrolides,J01FA08,Watch,No
Trovafloxacin,Fluoroquinolones,J01MA13,Watch,No
Vancomycin_IV,Glycopeptides,J01XA01,Watch,Yes
Vancomycin_oral,Glycopeptides,A07AA09,Watch,Yes
"""

    # Parse the CSV-like data
    data = []
    for line in data_lines.strip().split('\n'):
        parts = line.strip().split(',')
        if len(parts) >= 5:
            data.append({
                'Antibiotic': parts[0],
                'Class': parts[1],
                'ATC': parts[2],
                'Category': parts[3],
                'EML': parts[4]
            })

    # Create DataFrame
    df = pd.DataFrame(data)
    return df


# ALTERNATIVE: If you have the actual Excel file, use this function instead:
def load_drug_database_from_excel(file_path="WHO drug name classification.xlsx"):
    """Load drug database from Excel file"""
    try:
        # Read the main classification sheet
        df = pd.read_excel(
            file_path,
            sheet_name="AWaRe classification 2023",
            skiprows=3  # Skip header rows
        )

        # Clean up column names
        df.columns = ['Antibiotic', 'Class', 'ATC', 'Category', 'Listed on EML/EMLc 2023']

        # Rename columns for consistency
        df = df.rename(columns={'Listed on EML/EMLc 2023': 'EML'})

        # Clean up data
        df['EML'] = df['EML'].replace({'Yes': 'Yes', 'No': 'No'})

        return df
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        # Fall back to text data
        return create_drug_database_from_text()


# Load the drug database
drug_db = create_drug_database_from_text()


# Add search functionality
def search_drug(drug_name):
    """Search for a drug in the database with fuzzy matching"""
    drug_name_lower = drug_name.lower().strip()

    # Exact match
    exact_match = drug_db[drug_db['Antibiotic'].str.lower() == drug_name_lower]
    if not exact_match.empty:
        return exact_match

    # Try removing special characters and spaces
    drug_clean = drug_name_lower.replace('/', '').replace('-', '').replace(' ', '')
    for idx, row in drug_db.iterrows():
        db_drug_clean = row['Antibiotic'].lower().replace('/', '').replace('-', '').replace(' ', '')
        if drug_clean in db_drug_clean or db_drug_clean in drug_clean:
            return drug_db[drug_db.index == idx]

    # Try partial match
    partial_match = drug_db[drug_db['Antibiotic'].str.lower().str.contains(drug_name_lower)]
    if not partial_match.empty:
        return partial_match

    # Return empty DataFrame if no match
    return pd.DataFrame(columns=drug_db.columns)


# Create tabs for different input methods
tab1, tab2, tab3 = st.tabs(["📝 Single Drug Search", "📄 Batch Upload", "📊 Database View"])

with tab1:
    st.header("Search Single Drug")

    col1, col2 = st.columns([3, 1])

    with col1:
        drug_input = st.text_input(
            "Enter drug name:",
            placeholder="e.g., Amoxicillin, Ceftriaxone, Vancomycin..."
        )

    with col2:
        st.write("")
        st.write("")
        search_button = st.button("🔍 Search", use_container_width=True)

    if search_button and drug_input:
        results = search_drug(drug_input)

        if not results.empty:
            st.success(f"Found {len(results)} result(s) for '{drug_input}'")

            # Display results in a nice format
            for _, row in results.iterrows():
                with st.container():
                    # Color code based on category
                    if row['Category'] == 'Access':
                        color = "🟢"
                        badge_color = "#d4edda"
                        text_color = "#155724"
                    elif row['Category'] == 'Watch':
                        color = "🟡"
                        badge_color = "#fff3cd"
                        text_color = "#856404"
                    else:  # Reserve
                        color = "🔴"
                        badge_color = "#f8d7da"
                        text_color = "#721c24"

                    # Create a styled card
                    st.markdown(f"""
                    <div style="background-color:{badge_color}; padding:15px; border-radius:10px; border-left:5px solid {text_color}; margin:10px 0;">
                        <h4 style="color:{text_color}; margin:0;">{color} {row['Antibiotic']} - <strong>{row['Category']}</strong></h4>
                        <p style="margin:5px 0;"><strong>Class:</strong> {row['Class']}</p>
                        <p style="margin:5px 0;"><strong>ATC Code:</strong> {row['ATC']}</p>
                        <p style="margin:5px 0;"><strong>EML Status:</strong> {"✅ Yes" if row['EML'] == "Yes" else "❌ No"}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Additional details in expander
                    with st.expander("More Information"):
                        if row['Category'] == 'Access':
                            st.info("""
                            **Access Category:** 
                            First or second choice empiric treatment options for common infections.
                            Lower resistance potential compared to other groups.
                            """)
                        elif row['Category'] == 'Watch':
                            st.warning("""
                            **Watch Category:**
                            Higher resistance potential. Should be prioritized as key targets 
                            of stewardship programs and monitoring.
                            """)
                        else:
                            st.error("""
                            **Reserve Category:**
                            "Last resort" options for confirmed or suspected infections due to 
                            multi-drug-resistant organisms. Use should be highly restricted.
                            """)

                    st.divider()
        else:
            st.error(f"No results found for '{drug_input}'")
            st.info(
                "💡 **Tips:** Try using the exact drug name. Check spelling or browse the database tab for available drugs.")

with tab2:
    st.header("Batch Drug Classification")

    st.markdown("""
    Upload a file with a list of drug names (one per line) or paste them in the text area below.
    The app will classify each drug into its AWaRe category.
    """)

    # File upload option
    uploaded_file = st.file_uploader(
        "Choose a text file with drug names (one per line)",
        type=['txt', 'csv'],
        help="Upload a .txt or .csv file with one drug name per line"
    )

    # Text area for manual input
    drug_list_text = st.text_area(
        "Or paste drug names (one per line):",
        height=150,
        placeholder="Amoxicillin\nCeftriaxone\nVancomycin\nAzithromycin\n...",
        help="Enter one drug name per line"
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        process_button = st.button("🚀 Classify Drugs", use_container_width=True)

    if process_button:
        drugs_to_classify = []

        if uploaded_file is not None:
            # Read from uploaded file
            try:
                content = uploaded_file.getvalue().decode("utf-8")
                drugs_to_classify = [line.strip() for line in content.split('\n') if line.strip()]
                st.success(f"Read {len(drugs_to_classify)} drugs from file")
            except Exception as e:
                st.error(f"Error reading file: {e}")

        elif drug_list_text:
            # Read from text area
            drugs_to_classify = [line.strip() for line in drug_list_text.split('\n') if line.strip()]

        if drugs_to_classify:
            results = []
            not_found = []

            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()

            for i, drug in enumerate(drugs_to_classify):
                status_text.text(f"Processing {i + 1}/{len(drugs_to_classify)}: {drug}")
                progress_bar.progress((i + 1) / len(drugs_to_classify))

                found = search_drug(drug)
                if not found.empty:
                    # Take the first match if multiple found
                    drug_info = found.iloc[0].to_dict()
                    drug_info['Input Name'] = drug
                    results.append(drug_info)
                else:
                    not_found.append(drug)

            # Clear progress bar
            progress_bar.empty()
            status_text.empty()

            if results:
                # Create results DataFrame
                results_df = pd.DataFrame(results)
                results_df = results_df[['Input Name', 'Antibiotic', 'Category', 'Class', 'ATC', 'EML']]

                # Display summary
                st.success(f"✅ Classified {len(results)} out of {len(drugs_to_classify)} drugs")

                # Display results table with color coding
                st.subheader("Classification Results")


                # Define color mapping for the table
                def color_category(val):
                    if val == 'Access':
                        return 'background-color: #d4edda; color: #155724;'
                    elif val == 'Watch':
                        return 'background-color: #fff3cd; color: #856404;'
                    elif val == 'Reserve':
                        return 'background-color: #f8d7da; color: #721c24;'
                    return ''


                def color_eml(val):
                    if val == 'Yes':
                        return 'background-color: #d4edda; color: #155724;'
                    else:
                        return 'background-color: #f8d7da; color: #721c24;'


                # Apply styling
                styled_df = results_df.style.applymap(color_category, subset=['Category'])
                styled_df = styled_df.applymap(color_eml, subset=['EML'])

                st.dataframe(
                    styled_df,
                    use_container_width=True,
                    hide_index=True
                )

                # Add download button
                csv = results_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv,
                    file_name="aware_classification_results.csv",
                    mime="text/csv",
                    use_container_width=True
                )

                # Display statistics with charts
                st.subheader("📊 Classification Statistics")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    access_count = len(results_df[results_df['Category'] == 'Access'])
                    st.metric("Access", access_count, delta=None)

                with col2:
                    watch_count = len(results_df[results_df['Category'] == 'Watch'])
                    st.metric("Watch", watch_count, delta=None)

                with col3:
                    reserve_count = len(results_df[results_df['Category'] == 'Reserve'])
                    st.metric("Reserve", reserve_count, delta=None)

                with col4:
                    eml_count = len(results_df[results_df['EML'] == 'Yes'])
                    st.metric("On EML", eml_count, delta=None)

                # Create a simple bar chart
                if len(results_df) > 0:
                    category_counts = results_df['Category'].value_counts()
                    chart_data = pd.DataFrame({
                        'Category': category_counts.index,
                        'Count': category_counts.values
                    })
                    st.bar_chart(chart_data.set_index('Category'))

            if not_found:
                st.warning(f"⚠️ Could not find {len(not_found)} drug(s):")
                with st.expander("Show unrecognized drugs"):
                    st.write(", ".join(not_found))
                    st.info("These drugs were not found in the database. Check spelling or browse the database tab.")

        else:
            st.info("Please upload a file or enter drug names to classify.")

with tab3:
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
            default=["Access", "Watch", "Reserve"]
        )

    with col2:
        eml_filter = st.multiselect(
            "Filter by EML Status:",
            options=["Yes", "No"],
            default=["Yes", "No"]
        )

    with col3:
        search_db = st.text_input("Search in database:", placeholder="Search drug names or classes...")

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
            filtered_db['Class'].str.lower().str.contains(search_lower)
            ]

    # Display the database with color coding
    st.subheader(f"Showing {len(filtered_db)} of {len(drug_db)} drugs")


    # Define color mapping function
    def highlight_rows(row):
        if row['Category'] == 'Access':
            return ['background-color: #e8f5e9'] * len(row)
        elif row['Category'] == 'Watch':
            return ['background-color: #fffde7'] * len(row)
        else:  # Reserve
            return ['background-color: #ffebee'] * len(row)


    # Apply styling
    styled_db = filtered_db.style.apply(highlight_rows, axis=1)

    st.dataframe(
        styled_db,
        use_container_width=True,
        column_config={
            "Antibiotic": st.column_config.TextColumn(
                "Antibiotic",
                help="Name of the antibiotic"
            ),
            "Category": st.column_config.SelectboxColumn(
                "Category",
                options=["Access", "Watch", "Reserve"],
                help="AWaRe classification category"
            ),
            "Class": st.column_config.TextColumn(
                "Class",
                help="Pharmacological class of the antibiotic"
            ),
            "ATC": st.column_config.TextColumn(
                "ATC Code",
                help="Anatomical Therapeutic Chemical code"
            ),
            "EML": st.column_config.SelectboxColumn(
                "EML",
                options=["Yes", "No"],
                help="Included in WHO Essential Medicines List"
            )
        },
        hide_index=True
    )

    # Display database statistics
    st.subheader("📈 Database Statistics")

    total_drugs = len(drug_db)
    filtered_drugs = len(filtered_db)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Drugs", total_drugs)

    with col2:
        access_count = len(drug_db[drug_db['Category'] == 'Access'])
        st.metric("Access Drugs", access_count)

    with col3:
        watch_count = len(drug_db[drug_db['Category'] == 'Watch'])
        st.metric("Watch Drugs", watch_count)

    with col4:
        reserve_count = len(drug_db[drug_db['Category'] == 'Reserve'])
        st.metric("Reserve Drugs", reserve_count)

    # Category distribution chart
    st.subheader("Category Distribution")
    category_dist = drug_db['Category'].value_counts()

    # Create a pie chart using Streamlit
    chart_data = pd.DataFrame({
        'Category': category_dist.index,
        'Count': category_dist.values
    })

    # Display as columns
    cols = st.columns(3)
    for idx, (category, count) in enumerate(category_dist.items()):
        with cols[idx]:
            if category == 'Access':
                st.markdown(f"<h3 style='color:#4CAF50;'>🟢 {category}</h3>", unsafe_allow_html=True)
            elif category == 'Watch':
                st.markdown(f"<h3 style='color:#FFC107;'>🟡 {category}</h3>", unsafe_allow_html=True)
            else:
                st.markdown(f"<h3 style='color:#F44336;'>🔴 {category}</h3>", unsafe_allow_html=True)
            st.markdown(f"<h2>{count}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p>{count / total_drugs * 100:.1f}% of total</p>", unsafe_allow_html=True)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em;">
    <p><strong>WHO AWaRe Antibiotic Classification Tool</strong></p>
    <p>Based on WHO Access, Watch, Reserve (AWaRe) classification of antibiotics for evaluation and monitoring of use, 2023</p>
    <p>This tool is for informational purposes only. Always consult official guidelines for clinical decisions.</p>
</div>
""", unsafe_allow_html=True)