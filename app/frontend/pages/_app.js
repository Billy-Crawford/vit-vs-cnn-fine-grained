import '../styles/globals.css';

// Composant racine Next.js : injecte les styles globaux
// pour toutes les pages de l'application.
export default function App({ Component, pageProps }) {
  return <Component {...pageProps} />;
}