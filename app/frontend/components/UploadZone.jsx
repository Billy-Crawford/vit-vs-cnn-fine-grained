import { useCallback, useState } from "react";

export default function UploadZone({ onImageSelected }) {
  const [isDragging, setIsDragging] = useState(false);

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
        padding: "48px 32px",
        textAlign: "center",
        background: isDragging ? "rgba(63, 107, 79, 0.06)" : "var(--paper-card)",
        transition: "border-color 0.15s ease, background 0.15s ease",
      }}
    >
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
      <p style={{ margin: "0 0 20px", color: "var(--ink-soft)", fontSize: 15 }}>
        Déposez une photographie d&apos;oiseau ici
      </p>
      <label
        style={{
          display: "inline-block",
          padding: "10px 22px",
          background: "var(--ink)",
          color: "var(--paper)",
          borderRadius: 2,
          cursor: "pointer",
          fontSize: 13,
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
