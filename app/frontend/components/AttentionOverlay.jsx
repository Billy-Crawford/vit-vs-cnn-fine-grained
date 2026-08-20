export default function AttentionOverlay({ overlayBase64 }) {
  if (!overlayBase64) return null;

  return (
    <div
      style={{
        border: "1px solid var(--line)",
        borderRadius: 4,
        background: "var(--paper-card)",
        boxShadow: "var(--shadow-card)",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          padding: "10px 18px",
          borderBottom: "1px solid var(--line)",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-end",
          flexWrap: "wrap",
          gap: 12,
        }}
      >
        <div>
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

        {/* Légende du dégradé : sauge (faible attention) vers rouille (forte attention) */}
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: 10,
              color: "var(--sage-dim)",
            }}
          >
            faible
          </span>
          <div
            style={{
              width: 72,
              height: 6,
              borderRadius: 3,
              background:
                "linear-gradient(90deg, var(--sage-dim), var(--rust))",
            }}
          />
          <span
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: 10,
              color: "var(--rust)",
            }}
          >
            forte
          </span>
        </div>
      </div>

      <div style={{ padding: 18 }}>
        <img
          src={`data:image/png;base64,${overlayBase64}`}
          alt="Carte d'attention"
          style={{
            maxWidth: "100%",
            maxHeight: 520,
            margin: "0 auto",
            borderRadius: 2,
            display: "block",
          }}
        />
      </div>
    </div>
  );
}