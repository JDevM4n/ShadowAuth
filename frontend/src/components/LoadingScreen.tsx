type LoadingScreenProps = {
  title?: string;
  message?: string;
};

export default function LoadingScreen({
  title = "Loading ShadowAuth",
  message =
    "Connecting to security telemetry and preparing detection data.",
}: LoadingScreenProps) {
  return (
    <div
      className="loading-screen"
      role="status"
      aria-live="polite"
    >
      <div className="loading-card">
        <div className="loading-logo">
          <img
            src="/logo-shadowauth.png"
            alt="ShadowAuth logo"
            className="loading-logo-image"
          />
        </div>

        <div className="loading-spinner-wrapper">
          <div className="loading-spinner" />

          <div className="loading-spinner-core" />
        </div>

        <h2>{title}</h2>

        <p>{message}</p>

        <div
          className="loading-dots"
          aria-hidden="true"
        >
          <span />
          <span />
          <span />
        </div>
      </div>
    </div>
  );
}