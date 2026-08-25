import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Palette de couleurs modernes & professionnelles
    COLOR_PRIMARY = RGBColor(15, 23, 42)      # Navy sombre #0F172A
    COLOR_SECONDARY = RGBColor(30, 41, 59)    # Slate dark #1E293B
    COLOR_ACCENT = RGBColor(14, 165, 233)     # Cyan / Sky #0EA5E9
    COLOR_ACCENT_BLUE = RGBColor(37, 99, 235) # Royal Blue #2563EB
    COLOR_SUCCESS = RGBColor(16, 185, 129)    # Emerald #10B981
    COLOR_WARNING = RGBColor(245, 158, 11)    # Amber #F59E0B
    COLOR_TEXT_MAIN = RGBColor(15, 23, 42)    # Dark text
    COLOR_TEXT_MUTED = RGBColor(100, 116, 139)# Slate gray
    COLOR_WHITE = RGBColor(255, 255, 255)
    COLOR_BG_CARD = RGBColor(248, 250, 252)   # Light gray #F8FAFC
    COLOR_BORDER_CARD = RGBColor(226, 232, 240)

    blank_slide_layout = prs.slide_layouts[6]
    
    REPO_DIR = os.path.dirname(os.path.abspath(__file__))
    
    def add_header(slide, title, category="PROJET M1 IA — CLASSIFICATION FINE-GRAINED"):
        # Header category badge
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
        p_c = tf_c.paragraphs[0]
        p_c.text = category.upper()
        p_c.font.size = Pt(11)
        p_c.font.bold = True
        p_c.font.color.rgb = COLOR_ACCENT
        p_c.font.name = "Arial"
        
        # Header title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.65))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_PRIMARY
        p_t.font.name = "Arial"
        
        # Subtle horizontal bar
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.45), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_BORDER_CARD
        line.line.color.rgb = COLOR_BORDER_CARD

    def add_footer(slide, current_slide, total_slides=12):
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.3))
        tf = footer_box.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = f"ViT vs CNN — CUB-200-2011 | Master 1 IA | Soutenance finale                                                             Slide {current_slide}/{total_slides}"
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_TEXT_MUTED
        p.font.name = "Arial"

    def add_card(slide, left, top, width, height, bg_color=COLOR_BG_CARD, border_color=COLOR_BORDER_CARD):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    # =========================================================================
    # SLIDE 1 : TITRE & ACCUEIL
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_slide_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_PRIMARY
    bg1.line.fill.background()

    # Title box
    tbox = slide1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.333), Inches(3.5))
    tf1 = tbox.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "MASTER 1 INTELLIGENCE ARTIFICIELLE — PROJET ANNUEL"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    p.font.name = "Arial"
    p.space_after = Pt(14)
    
    p2 = tf1.add_paragraph()
    p2.text = "Vision Transformer vs CNN"
    p2.font.size = Pt(40)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE
    p2.font.name = "Arial"
    
    p3 = tf1.add_paragraph()
    p3.text = "Étude comparative sur la classification fine-grained d'images (CUB-200-2011)"
    p3.font.size = Pt(20)
    p3.font.color.rgb = RGBColor(203, 213, 225)
    p3.font.name = "Arial"
    p3.space_before = Pt(8)
    p3.space_after = Pt(24)
    
    # Équipe box
    add_card(slide1, Inches(1.0), Inches(4.7), Inches(11.333), Inches(1.8), bg_color=COLOR_SECONDARY, border_color=COLOR_ACCENT_BLUE)
    team_box = slide1.shapes.add_textbox(Inches(1.3), Inches(4.85), Inches(10.7), Inches(1.5))
    tf_team = team_box.text_frame
    tf_team.word_wrap = True
    
    pt = tf_team.paragraphs[0]
    pt.text = "RÉPARTITION DU TRAVAIL & MEMBRES DE L'ÉQUIPE :"
    pt.font.size = Pt(12)
    pt.font.bold = True
    pt.font.color.rgb = COLOR_ACCENT
    pt.space_after = Pt(8)
    
    p_roles = tf_team.add_paragraph()
    p_roles.text = "• Rôle A — Data / Experiment Engineer : SONHOUIN Abdoul-raouf\n• Rôle B — Model / Research Engineer : Ingénieur Modélisation\n• Rôle C — Reporting / Backend Developer : Développeur Déploiement & Fullstack"
    p_roles.font.size = Pt(13)
    p_roles.font.color.rgb = COLOR_WHITE
    p_roles.font.name = "Arial"
    
    slide1.notes_slide.notes_text_frame.text = (
        "Bonjour Monsieur le professeur. Nous vous présentons aujourd'hui notre projet annuel comparant les "
        "Vision Transformers (ViT) et les réseaux convolutifs (CNN, ResNet-50) sur une tâche de classification "
        "fine-grained d'oiseaux sur le dataset CUB-200-2011. Nous avons mené une étude d'ablation rigoureuse et développé "
        "une application web complète dockerisée pour mettre en démonstration nos modèles."
    )

    # =========================================================================
    # SLIDE 2 : CONTEXTE & PROBLÉMATIQUE
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide2, "1. Contexte & Problématique Scientifique")
    add_footer(slide2, 2)
    
    # 3 Cards
    # Card 1: Qu'est-ce que le fine-grained ?
    add_card(slide2, Inches(0.8), Inches(1.7), Inches(3.64), Inches(4.9))
    c1 = slide2.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(3.24), Inches(4.5))
    tfc1 = c1.text_frame
    tfc1.word_wrap = True
    p = tfc1.paragraphs[0]
    p.text = "🔍 Défi Fine-Grained"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT_BLUE
    p.space_after = Pt(12)
    
    p = tfc1.add_paragraph()
    p.text = "• Différences inter-classes minimes :\n  Subtiles variations de plumage, couleur de bec, motifs de queue.\n\n• Forte variabilité intra-classe :\n  Poses, éclairages, saisons, angles de vue.\n\n• Objectif :\n  Extraire et amplifier des indices visuels locaux très subtils."
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_TEXT_MAIN

    # Card 2: Biais inductif CNN vs ViT
    add_card(slide2, Inches(4.84), Inches(1.7), Inches(3.64), Inches(4.9))
    c2 = slide2.shapes.add_textbox(Inches(5.04), Inches(1.9), Inches(3.24), Inches(4.5))
    tfc2 = c2.text_frame
    tfc2.word_wrap = True
    p = tfc2.paragraphs[0]
    p.text = "🧠 Deux Paradigmes"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT_BLUE
    p.space_after = Pt(12)
    
    p = tfc2.add_paragraph()
    p.text = "• CNN (ResNet-50) :\n  Biais inductif fort : localité spatiale et invariance par translation.\n  Très efficace sur datasets restreints.\n\n• ViT (Vision Transformer) :\n  Séquence de patchs + Self-Attention globale sans a priori de localité.\n  Flexibilité maximale mais absence de biais inductif."
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_TEXT_MAIN

    # Card 3: Hypothèse et questions de recherche
    add_card(slide2, Inches(8.88), Inches(1.7), Inches(3.64), Inches(4.9))
    c3 = slide2.shapes.add_textbox(Inches(9.08), Inches(1.9), Inches(3.24), Inches(4.5))
    tfc3 = c3.text_frame
    tfc3.word_wrap = True
    p = tfc3.paragraphs[0]
    p.text = "🎯 Questions Clés"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT_BLUE
    p.space_after = Pt(12)
    
    p = tfc3.add_paragraph()
    p.text = "1. Le ViT peut-il rivaliser avec le CNN sur petit dataset sans pré-entraînement ?\n\n2. Quel est l'impact de la taille des patchs (16 vs 32) sur les détails fins ?\n\n3. Quelle est la courbe de sensibilité à la quantité de données (10% à 100%) ?"
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_TEXT_MAIN
    
    slide2.notes_slide.notes_text_frame.text = (
        "La classification fine-grained sur CUB-200 est très différente d'un ImageNet classique. "
        "Les classes sont très proches (par exemple 10 espèces de moineaux distinctes). "
        "Le CNN a un biais inductif de localité. Le ViT voit l'image comme des patchs et n'a pas cet a priori. "
        "Notre objectif est de quantifier expérimentalement ce comportement data-hungry."
    )

    # =========================================================================
    # SLIDE 3 : DATA PIPELINE & EDA (RÔLE A)
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide3, "2. Pipeline de Données & EDA (Rôle A)", "RÔLE A — DATA / EXPERIMENT ENGINEER")
    add_footer(slide3, 3)

    # Left text box
    add_card(slide3, Inches(0.8), Inches(1.7), Inches(5.6), Inches(4.9))
    c_data = slide3.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.2), Inches(4.6))
    tfc_d = c_data.text_frame
    tfc_d.word_wrap = True
    
    p = tfc_d.paragraphs[0]
    p.text = "Dataset CUB-200-2011 & Préparation"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)
    
    p = tfc_d.add_paragraph()
    p.text = "• 11 788 images réparties sur 200 espèces d'oiseaux.\n• Split stratifié & reproductible (seed=42) :\n   - Train : 5 094 images (100%)\n   - Validation : 900 images\n   - Test : 5 794 images (split officiel)\n• Sous-splits data-hungry créés : 10%, 25%, 50%, 100% du train.\n• Prétraitement : Redimensionnement 224×224 + Normalisation ImageNet.\n• Augmentations PyTorch :\n   - Faible : RandomHorizontalFlip, RandomResizedCrop\n   - Forte : ColorJitter, RandomRotation, RandomErasing"
    p.font.size = Pt(12.5)
    p.font.color.rgb = COLOR_TEXT_MAIN

    # Right: Image EDA
    img_path_eda = os.path.join(REPO_DIR, "data", "data_processed", "figures", "eda_similar_classes.png")
    if os.path.exists(img_path_eda):
        add_card(slide3, Inches(6.7), Inches(1.7), Inches(5.8), Inches(4.9))
        slide3.shapes.add_picture(img_path_eda, Inches(6.85), Inches(1.85), Inches(5.5), Inches(4.5))
    else:
        add_card(slide3, Inches(6.7), Inches(1.7), Inches(5.8), Inches(4.9))
        c_eda = slide3.shapes.add_textbox(Inches(6.9), Inches(2.0), Inches(5.4), Inches(4.2))
        c_eda.text_frame.text = "Illustration EDA CUB-200 (Classes similaires)"

    slide3.notes_slide.notes_text_frame.text = (
        "Le rôle A a structuré l'ensemble du dataset. Nous avons créé un split train/val/test rigoureux et stratifié "
        "pour que les 200 classes soient présentes même dans le sous-ensemble à 10%. Nous avons mis en place deux "
        "pipelines d'augmentation (faible et forte) et vérifié la distribution des images."
    )

    # =========================================================================
    # SLIDE 4 : ARCHITECTURES & PROTOCOLE (RÔLE B)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide4, "3. Modélisation & Protocole Expérimental (Rôle B)", "RÔLE B — MODEL / RESEARCH ENGINEER")
    add_footer(slide4, 4)

    # Card 1: Architectures
    add_card(slide4, Inches(0.8), Inches(1.7), Inches(5.6), Inches(4.9))
    c_arch = slide4.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.2), Inches(4.6))
    tf_arch = c_arch.text_frame
    tf_arch.word_wrap = True
    
    p = tf_arch.paragraphs[0]
    p.text = "Architectures Comparées"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)
    
    p = tf_arch.add_paragraph()
    p.text = "1. ResNet-50 (Pré-entraîné ImageNet)\n   • Backbone convolutif torchvision (23.9M params)\n   • Tête FC adaptée à 200 classes\n\n2. ViT Pré-entraîné (timm vit_small_patch16/32_224)\n   • Backbone pré-entraîné ImageNet-1k (21.7M - 22.6M params)\n   • Fine-tuning avec tête linéaire 200 sorties\n\n3. ViT from Scratch (Implémentation Custom)\n   • Patch embedding (patch 16 / 32) + [CLS] token\n   • Positional embeddings appris\n   • 6 Blocs Transformer (384 dim, 6 heads, MLP ratio 4)\n   • 11.1M paramètres — aucun poids pré-entraîné"
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_TEXT_MAIN

    # Card 2: Protocole & MLflow
    add_card(slide4, Inches(6.7), Inches(1.7), Inches(5.8), Inches(4.9))
    c_proto = slide4.shapes.add_textbox(Inches(6.9), Inches(1.85), Inches(5.4), Inches(4.6))
    tf_proto = c_proto.text_frame
    tf_proto.word_wrap = True
    
    p = tf_proto.paragraphs[0]
    p.text = "Protocole d'Entraînement & Tracking"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)
    
    p = tf_proto.add_paragraph()
    p.text = "• Optimiseur : AdamW (lr = 1e-4, weight decay = 0.01)\n• Fonction de perte : Cross-Entropy Loss\n• Batch size : 32 | Résolution : 224×224\n• Durée : 3 époques (contrainte de temps de calcul)\n• Checkpointing automatique : meilleur modèle sauvé sur Val Acc\n• Seed fixe : 42 sur l'ensemble des runs\n\n🔬 Suivi & Traçabilité MLflow :\n• 12 configurations enregistrées dans mlflow.db\n• Sauvegarde des hyperparamètres, loss, top-1, top-5\n• Modèles complets packagés et visualisables sur MLflow UI."
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_TEXT_MAIN

    slide4.notes_slide.notes_text_frame.text = (
        "Le rôle B a codé les 3 modèles. Le ViT scratch a été implémenté de zéro (patch embedding, multi-head attention, "
        "positional embedding). Nous avons harmonisé l'optimiseur (AdamW lr 1e-4) et suivi l'ensemble des 12 expériences "
        "avec MLflow pour une traçabilité irréprochable."
    )

    # =========================================================================
    # SLIDE 5 : RÉSULTATS GLOBAUX DE L'ÉTUDE
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide5, "4. Résultats Globaux des 12 Configurations", "RÉSULTATS EXPÉRIMENTAUX")
    add_footer(slide5, 5)

    # Table des résultats
    rows = 8
    cols = 5
    table_shape = slide5.shapes.add_table(rows, cols, Inches(0.8), Inches(1.7), Inches(11.733), Inches(4.9))
    table = table_shape.table
    
    # Column widths
    table.columns[0].width = Inches(4.3)
    table.columns[1].width = Inches(1.8)
    table.columns[2].width = Inches(1.8)
    table.columns[3].width = Inches(1.8)
    table.columns[4].width = Inches(2.033)
    
    headers = ["Configuration / Modèle", "Top-1 Acc.", "Top-5 Acc.", "Test Loss", "Paramètres"]
    for c_idx, h in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER
        
    data_table = [
        ["ResNet-50 (Pré-entraîné — 100% data)", "71.87 %", "93.58 %", "1.05", "23.9 M"],
        ["ResNet-50 (Pré-entraîné — 50% data)", "48.74 %", "81.12 %", "2.09", "23.9 M"],
        ["ResNet-50 (Pré-entraîné — 25% data)", "23.47 %", "48.88 %", "3.65", "23.9 M"],
        ["ResNet-50 (Pré-entraîné — 10% data)", "5.11 %", "13.95 %", "5.13", "23.9 M"],
        ["ViT Pré-entraîné (Patch 32 — 100% data)", "53.85 %", "83.50 %", "1.81", "22.6 M"],
        ["ViT Pré-entraîné (Patch 16 — 100% data)", "9.94 %", "25.37 %", "4.65", "21.7 M"],
        ["ViT from Scratch (100% data — Patch 16/32)", "1.07 % - 2.00 %", "4.75 % - 8.46 %", "~5.15", "11.1 M"],
    ]
    
    for r_idx, row_data in enumerate(data_table):
        for c_idx, val in enumerate(row_data):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            # Highlight best models
            if r_idx == 0:
                cell.fill.fore_color.rgb = RGBColor(240, 253, 244) # Very soft green
            elif r_idx == 4:
                cell.fill.fore_color.rgb = RGBColor(238, 242, 255) # Very soft blue
            else:
                cell.fill.fore_color.rgb = COLOR_WHITE if r_idx % 2 == 0 else COLOR_BG_CARD
                
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(12)
            p.font.name = "Arial"
            if c_idx == 0:
                p.alignment = PP_ALIGN.LEFT
                if r_idx in [0, 4]:
                    p.font.bold = True
            else:
                p.alignment = PP_ALIGN.CENTER
                if c_idx == 1 and r_idx == 0:
                    p.font.bold = True
                    p.font.color.rgb = COLOR_SUCCESS

    slide5.notes_slide.notes_text_frame.text = (
        "Voici le tableau récapitulatif testé sur les 5 794 images de test. "
        "ResNet-50 pré-entraîné atteint 71.87% en Top-1 et 93.58% en Top-5. "
        "Le ViT pré-entraîné patch 32 monte à 53.85% (83.50% top-5). "
        "Le ViT scratch reste bloqué à ~1-2% en 3 époques."
    )

    # =========================================================================
    # SLIDE 6 : ÉTUDE D'ABLATION 1 — SENSIBILITÉ AUX DONNÉES (DATA-HUNGRY)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide6, "5. Étude d'Ablation : Comportement « Data-Hungry »", "ÉTUDE D'ABLATION & ANALYSES")
    add_footer(slide6, 6)

    # Left: Text explanation
    add_card(slide6, Inches(0.8), Inches(1.7), Inches(5.6), Inches(4.9))
    c_dh = slide6.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.2), Inches(4.6))
    tf_dh = c_dh.text_frame
    tf_dh.word_wrap = True
    
    p = tf_dh.paragraphs[0]
    p.text = "Impact de la quantité de données"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)
    
    p = tf_dh.add_paragraph()
    p.text = "📈 Progression de ResNet-50 :\n• 10% des données (509 imgs) : 5.11 % Top-1\n• 25% des données (1 273 imgs) : 23.47 % Top-1\n• 50% des données (2 547 imgs) : 48.74 % Top-1\n• 100% des données (5 094 imgs) : 71.87 % Top-1\n→ Croissance strictement monotone grâce au biais inductif de convolution.\n\n📉 Stagnation du ViT from Scratch :\n• Reste bloqué à ~1% - 2% de 10% à 100% de données.\n→ Confirme la théorie de Dosovitskiy et al. : sans pré-entraînement massif, le Transformer n'a pas assez de données pour structurer son attention spatiale sur 5 094 images."
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_TEXT_MAIN

    # Right: Curve Image
    img_path_dh = os.path.join(REPO_DIR, "report", "figures", "data_hungry_curve.png")
    if os.path.exists(img_path_dh):
        add_card(slide6, Inches(6.7), Inches(1.7), Inches(5.8), Inches(4.9))
        slide6.shapes.add_picture(img_path_dh, Inches(6.85), Inches(1.85), Inches(5.5), Inches(4.5))

    slide6.notes_slide.notes_text_frame.text = (
        "Cette slide est le cœur théorique de notre soutenance. La courbe illustre parfaitement "
        "la différence fondamentale : le CNN apprend de manière monotone et solide même à 10% de données. "
        "Le ViT from scratch, dépourvu d'a priori inductif, est incapable de converger sur 5 000 images sans pré-entraînement."
    )

    # =========================================================================
    # SLIDE 7 : ÉTUDE D'ABLATION 2 — PRÉ-ENTRAÎNEMENT & PATCH SIZE
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide7, "6. Étude d'Ablation : Pré-entraînement & Taille de Patch", "ÉTUDE D'ABLATION & ANALYSES")
    add_footer(slide7, 7)

    # Left: Text
    add_card(slide7, Inches(0.8), Inches(1.7), Inches(5.6), Inches(4.9))
    c_ab2 = slide7.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.2), Inches(4.6))
    tf_ab2 = c_ab2.text_frame
    tf_ab2.word_wrap = True
    
    p = tf_ab2.paragraphs[0]
    p.text = "Observations Clés sur le ViT"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)
    
    p = tf_ab2.add_paragraph()
    p.text = "1. Le pré-entraînement est un prérequis absolu pour le ViT :\n• ViT Scratch : 1.07 % Top-1\n• ViT Pré-entraîné Patch 32 : 53.85 % Top-1 (+52.78 points)\n\n2. Comparaison Taille de Patch (16 vs 32) :\n• Théorie : Patch 16 (196 patchs) = granularité plus fine idéale pour le fine-grained.\n• Résultats empiriques :\n   - Patch 32 : 53.85 % Top-1 | 83.50 % Top-5\n   - Patch 16 : 9.94 % Top-1 | 25.37 % Top-5\n• Analyse : Patch 16 engendre une séquence 4× plus longue (196 vs 49 tokens), nécessitant un learning rate adapté et plus d'époques pour converger."
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_TEXT_MAIN

    # Right: Comparison Image
    img_path_comp = os.path.join(REPO_DIR, "results", "figures", "final_model_comparison.png")
    if os.path.exists(img_path_comp):
        add_card(slide7, Inches(6.7), Inches(1.7), Inches(5.8), Inches(4.9))
        slide7.shapes.add_picture(img_path_comp, Inches(6.85), Inches(1.85), Inches(5.5), Inches(4.5))

    slide7.notes_slide.notes_text_frame.text = (
        "Le pré-entraînement fait passer le ViT de 1% à 53.85%. "
        "Concernant la taille de patch : le patch 32 performe mieux en 3 époques car il a 49 tokens au lieu de 196, "
        "rendant l'attention beaucoup plus rapide à adapter lors d'un fine-tuning court."
    )

    # =========================================================================
    # SLIDE 8 : APPLICATION & CARTE D'ATTENTION (RÔLE C)
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide8, "7. Application de Démonstration & Interprétabilité (Rôle C)", "RÔLE C — BACKEND & APPLICATION FULLSTACK")
    add_footer(slide8, 8)

    # Card 1: Architecture App
    add_card(slide8, Inches(0.8), Inches(1.7), Inches(5.6), Inches(4.9))
    c_app = slide8.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.2), Inches(4.6))
    tf_app = c_app.text_frame
    tf_app.word_wrap = True
    
    p = tf_app.paragraphs[0]
    p.text = "Architecture Fullstack & Attention"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)
    
    p = tf_app.add_paragraph()
    p.text = "• Backend FastAPI (Python 3.11) :\n   - /predict : Inférence simultanée ViT & ResNet-50 (Top-3 + probabilités)\n   - /attention : Heatmap d'attention réelle du ViT\n   - /classes : Mapping des 200 espèces CUB\n\n• Frontend Next.js 14 (React) :\n   - Interface interactive avec drag & drop d'image\n   - Visualisation comparative côte-à-côte\n   - Indicateur d'accord / désaccord entre modèles\n\n• Extraction de l'attention réelle :\n   - Hook PyTorch interceptant attn_drop sur le dernier bloc ViT\n   - Ligne du token [CLS] moyennée sur les têtes et projetée en grille 2D."
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_TEXT_MAIN

    # Right: Nominal App Image
    img_path_nom = os.path.join(REPO_DIR, "report", "figures", "app_nominal.png")
    if os.path.exists(img_path_nom):
        add_card(slide8, Inches(6.7), Inches(1.7), Inches(5.8), Inches(4.9))
        slide8.shapes.add_picture(img_path_nom, Inches(6.85), Inches(1.85), Inches(5.5), Inches(4.5))

    slide8.notes_slide.notes_text_frame.text = (
        "Le rôle C a conçu l'application de démonstration. Nous avons développé une extraction réelle "
        "des cartes d'attention du ViT : on intercepte les poids d'auto-attention du token CLS vers les patchs "
        "de l'image pour afficher exactement sur quelle zone anatomique l'attention s'est focalisée."
    )

    # =========================================================================
    # SLIDE 9 : CAS NOMINAL VS HORS-DISTRIBUTION (OOD)
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide9, "8. Robustesse & Détection Hors-Distribution (OOD)", "DÉPLOIEMENT & VALIDATION QUALITATIVE")
    add_footer(slide9, 9)

    # Left: Explication
    add_card(slide9, Inches(0.8), Inches(1.7), Inches(5.6), Inches(4.9))
    c_ood = slide9.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.2), Inches(4.6))
    tf_ood = c_ood.text_frame
    tf_ood.word_wrap = True
    
    p = tf_ood.paragraphs[0]
    p.text = "Comportement face à l'inconnu"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)
    
    p = tf_ood.add_paragraph()
    p.text = "✅ Cas Nominal (Image de Test CUB) :\n• Espèce : Gray-crowned Rosy Finch\n• Résultat : Accord total entre ViT et ResNet-50.\n• Confiance élevée (ResNet: 83.4%, ViT: 26.5%).\n\n⚠️ Cas Hors-Distribution (OOD) :\n• Test avec une espèce absente du dataset (Rouge-gorge européen).\n• Résultat : Confiance très faible et désaccord entre les deux modèles.\n• Bénéfice : Signal clair d'incertitude plutôt qu'une erreur silencieuse à haute confiance."
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_TEXT_MAIN

    # Right: OOD Image
    img_path_ood = os.path.join(REPO_DIR, "report", "figures", "app_ood.png")
    if os.path.exists(img_path_ood):
        add_card(slide9, Inches(6.7), Inches(1.7), Inches(5.8), Inches(4.9))
        slide9.shapes.add_picture(img_path_ood, Inches(6.85), Inches(1.85), Inches(5.5), Inches(4.5))

    slide9.notes_slide.notes_text_frame.text = (
        "Nous avons testé la robustesse du système sur des données hors-distribution. "
        "En injectant un oiseau absent de CUB-200, les modèles divergent et la confiance s'effondre, "
        "ce qui constitue un excellent garde-fou pour un déploiement réel."
    )

    # =========================================================================
    # SLIDE 10 : INDUSTRIALISATION & DOCKERISATION
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide10, "9. Déploiement & Dockerisation Reproductible", "INGÉNIERIE LOGICIELLE & DÉPLOIEMENT")
    add_footer(slide10, 10)

    # 3 Cards
    # Card 1: Backend Docker
    add_card(slide10, Inches(0.8), Inches(1.7), Inches(3.64), Inches(4.9))
    c_d1 = slide10.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(3.24), Inches(4.5))
    tf_d1 = c_d1.text_frame
    tf_d1.word_wrap = True
    p = tf_d1.paragraphs[0]
    p.text = "🐳 Backend Docker"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT_BLUE
    p.space_after = Pt(12)
    
    p = tf_d1.add_paragraph()
    p.text = "• Python 3.11-slim optimisé CPU\n• PyTorch CPU sans surcoût CUDA (images légères)\n• Utilisateur non-root sécurisé\n• Healthcheck HTTP sur /health\n• Inférence rapide sur CPU"
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_TEXT_MAIN

    # Card 2: Frontend Standalone
    add_card(slide10, Inches(4.84), Inches(1.7), Inches(3.64), Inches(4.9))
    c_d2 = slide10.shapes.add_textbox(Inches(5.04), Inches(1.9), Inches(3.24), Inches(4.5))
    tf_d2 = c_d2.text_frame
    tf_d2.word_wrap = True
    p = tf_d2.paragraphs[0]
    p.text = "⚡ Frontend Multi-Stage"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT_BLUE
    p.space_after = Pt(12)
    
    p = tf_d2.add_paragraph()
    p.text = "• Build multi-stage Node 20 Alpine\n• Mode output: 'standalone'\n• Dépendances de build isolées\n• Serveur Node ultra-léger\n• Injection dynamique d'API URL"
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_TEXT_MAIN

    # Card 3: Compose & Multi-OS
    add_card(slide10, Inches(8.88), Inches(1.7), Inches(3.64), Inches(4.9))
    c_d3 = slide10.shapes.add_textbox(Inches(9.08), Inches(1.9), Inches(3.24), Inches(4.5))
    tf_d3 = c_d3.text_frame
    tf_d3.word_wrap = True
    p = tf_d3.paragraphs[0]
    p.text = "🚀 Orchestration Compose"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT_BLUE
    p.space_after = Pt(12)
    
    p = tf_d3.add_paragraph()
    p.text = "• Lancement 1-clic : docker compose up -d\n• Synchronisation : frontend attend healthcheck backend\n• Profil MLflow UI optionnel\n• Garantie zéro conflit d'OS (Windows, macOS, Linux)"
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_TEXT_MAIN

    slide10.notes_slide.notes_text_frame.text = (
        "Pour garantir la portabilité et la reproductibilité totale, nous avons dockerisé l'ensemble du projet. "
        "Le backend tourne sur un PyTorch CPU optimisé, le frontend est compilé en multi-stage standalone, "
        "et Docker Compose gère la synchronisation avec des healthchecks."
    )

    # =========================================================================
    # SLIDE 11 : LIMITES & PERSPECTIVES
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide11, "10. Discussion, Limites & Perspectives", "ANALYSE CRITIQUE")
    add_footer(slide11, 11)

    # Card 1: Limites
    add_card(slide11, Inches(0.8), Inches(1.7), Inches(5.6), Inches(4.9))
    c_lim = slide11.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.2), Inches(4.6))
    tf_lim = c_lim.text_frame
    tf_lim.word_wrap = True
    
    p = tf_lim.paragraphs[0]
    p.text = "⚠️ Limites Identifiées"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_WARNING
    p.space_after = Pt(10)
    
    p = tf_lim.add_paragraph()
    p.text = "• Nombre d'époques restreint (3 époques) :\n   Contrainte de calcul qui pénalise fortement le ViT scratch (sous-entraînement).\n\n• Taille du modèle ViT scratch :\n   6 blocs et 384 dim (11.1M params), plus petit qu'un ViT-Base standard.\n\n• Écart Patch 16 vs Patch 32 :\n   Convergence plus lente du patch 16 sur 3 époques méritant un tuning d'hyperparamètres dédié.\n\n• Absence d'évaluation de variance :\n   Un seul seed d'entraînement (seed=42) par configuration."
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_TEXT_MAIN

    # Card 2: Perspectives
    add_card(slide11, Inches(6.7), Inches(1.7), Inches(5.8), Inches(4.9))
    c_per = slide11.shapes.add_textbox(Inches(6.9), Inches(1.85), Inches(5.4), Inches(4.6))
    tf_per = c_per.text_frame
    tf_per.word_wrap = True
    
    p = tf_per.paragraphs[0]
    p.text = "💡 Perspectives & Outils Développés"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_SUCCESS
    p.space_after = Pt(10)
    
    p = tf_per.add_paragraph()
    p.text = "• Pipeline d'entraînement avancé déjà codé :\n   - Scheduler Cosine Annealing avec Warmup\n   - Précision mixte automatique (AMP fp16)\n   - Mécanisme d'Early Stopping\n\n• Évolutions futures :\n   - Entraînement long sur GPU (50 à 100 époques)\n   - Distillation de connaissances (DeiT)\n   - Intégration de parties de l'oiseau (Part-based attention) pour guider le Transformer sur les zones critiques (bec, ailes)."
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_TEXT_MAIN

    slide11.notes_slide.notes_text_frame.text = (
        "En conclusion critique, la principale limite est le budget de 3 époques. "
        "Nous avons déjà implémenté dans le code du projet les outils pour aller plus loin : scheduler, AMP, early stopping. "
        "Une perspective prometteuse serait d'utiliser la distillation (DeiT) pour compenser le manque de données du ViT."
    )

    # =========================================================================
    # SLIDE 12 : CONCLUSION & QUESTIONS
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_slide_layout)
    bg12 = slide12.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg12.fill.solid()
    bg12.fill.fore_color.rgb = COLOR_PRIMARY
    bg12.line.fill.background()

    # Center Box
    c_fin = slide12.shapes.add_textbox(Inches(1.5), Inches(1.5), Inches(10.333), Inches(4.5))
    tf_fin = c_fin.text_frame
    tf_fin.word_wrap = True
    
    p = tf_fin.paragraphs[0]
    p.text = "SYNTHÈSE DU PROJET"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    p.alignment = PP_ALIGN.CENTER
    p.space_after = Pt(14)
    
    p = tf_fin.add_paragraph()
    p.text = "Merci pour votre attention !"
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER
    p.space_after = Pt(20)
    
    p = tf_fin.add_paragraph()
    p.text = "Points Clés à Retenir :\n1. ResNet-50 domine sur petit jeu de données (71.9% Top-1) grâce à son biais inductif.\n2. Le ViT nécessite impérativement un pré-entraînement pour la classification fine-grained (53.9% vs 1.1%).\n3. Solution complète livrée : pipeline data, modèles PyTorch, MLflow, API FastAPI, Frontend Next.js et Docker."
    p.font.size = Pt(15)
    p.font.color.rgb = RGBColor(226, 232, 240)
    p.alignment = PP_ALIGN.CENTER
    p.space_after = Pt(24)
    
    p = tf_fin.add_paragraph()
    p.text = "Place aux questions & démonstration en direct"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    p.alignment = PP_ALIGN.CENTER

    slide12.notes_slide.notes_text_frame.text = (
        "Merci Monsieur le professeur. Nous sommes maintenant disponibles pour répondre à toutes vos questions "
        "et vous faire une démonstration en direct sur l'application web."
    )

    output_path = os.path.join(REPO_DIR, "presentation_vit_vs_cnn.pptx")
    prs.save(output_path)
    print(f"Presentation generated successfully at: {output_path}")

if __name__ == "__main__":
    create_presentation()
