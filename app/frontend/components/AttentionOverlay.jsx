export default function AttentionOverlay({ overlayBase64 }) {
  if (!overlayBase64) return null;

  return (
    <div
      style={{
        border: "1px solid var(--line)",
        borderRadius: 4,
        background: "var(--paper-card)",
        marginTop: 20,
        overflow: "hidden",
      }}
    >
      <div
        style={{
          padding: "10px 18px",
          borderBottom: "1px solid var(--line)",
        }}
      >
        <p
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: 10,
            letterSpacing: "0.1em",
            textTransform: "uppercase",
            color: "var(--sage-dim)",
            margin: "0 0 4px",
          }}
        >
          Fig. 02 — Zone d&apos;attention
        </p>
        <p style={{ margin: 0, fontSize: 13, color: "var(--ink-soft)" }}>
          Régions de l&apos;image ayant guidé la décision du ViT
        </p>
      </div>
      <div style={{ padding: 18 }}>
        <img
          src={`data:image/png;base64,${overlayBase64}`}
          alt="Carte d'attention"
          style={{ maxWidth: "100%", borderRadius: 2, display: "block" }}
        />
      </div>
    </div>
  );
}
