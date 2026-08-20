import { useCallback, useState } from "react";

/**
 * Zone de dépôt (drag & drop ou sélection manuelle) d'une photographie.
 *
 * Props :
 * - onImageSelected(file) : appelé avec le fichier choisi, si c'est une image.
 * - hasSelection : true une fois qu'un spécimen a déjà été déposé — la zone
 *   passe alors dans un mode compact ("déposez-en un autre pour remplacer")
 *   afin de laisser la place à la fiche du spécimen affichée en dessous.
 */
export default function UploadZone({ onImageSelected, hasSelection = false }) {
  const [isDragging, setIsDragging] = useState(false);

  // Ne retient que les fichiers dont le type MIME commence par "image/"
  const handleFile = useCallback(
    (file) => {
      if (!file || !file.type.startsWith("image/")) return;
      onImageSelected(file);
    },
    [onImageSelected]
  );

  const handleDrop = useCallback(
    (e) => {
      e.preventDefault();
      setIsDragging(false);
      handleFile(e.dataTransfer.files?.[0]);
    },
    [handleFile]
  );

  return (
    <div
      onDragOver={(e) => {
        e.preventDefault();
        setIsDragging(true);
      }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={handleDrop}
      style={{
        border: `1.5px dashed ${isDragging ? "var(--sage)" : "var(--line-strong)"}`,
        borderRadius: 4,
        // Mode compact : moins de hauteur une fois qu'une fiche spécimen
        // est déjà affichée en dessous, pour ne pas dupliquer l'emphase visuelle.
        padding: hasSelection ? "22px 20px" : "48px 24px",
        textAlign: "center",
        background: isDragging ? "var(--sage-wash)" : "var(--paper-card)",
        transition: "border-color 0.15s ease, background 0.15s ease",
      }}
    >
      {!hasSelection && (
        <p
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: 11,
            letterSpacing: "0.12em",
            textTransform: "uppercase",
            color: "var(--sage-dim)",
            margin: "0 0 12px",
          }}
        >
          Fig. 01 — Spécimen à identifier
        </p>
      )}

      <p
        style={{
          margin: hasSelection ? "0 0 14px" : "0 0 20px",
          color: "var(--ink-soft)",
          fontSize: hasSelection ? 12.5 : 15,
        }}
      >
        {hasSelection
          ? "Déposez une autre photo pour remplacer le spécimen actuel"
          : "Déposez une photographie d'oiseau ici"}
      </p>

      <label
        style={{
          display: "inline-block",
          padding: hasSelection ? "8px 18px" : "10px 22px",
          background: "var(--ink)",
          color: "var(--paper)",
          borderRadius: 2,
          cursor: "pointer",
          fontSize: hasSelection ? 12 : 13,
          fontWeight: 500,
          letterSpacing: "0.02em",
        }}
      >
        Choisir un fichier
        <input
          type="file"
          accept="image/jpeg,image/png,image/webp"
          onChange={(e) => handleFile(e.target.files?.[0])}
          style={{ display: "none" }}
        />
      </label>
    </div>
  );
}