const RightStatsPanel = () => {
  return (
    <aside className="stats-panel">
      <header className="stats-panel__header">
        <h1 className="stats-panel__title">Arctic Ice Metrics</h1>
        <p className="stats-panel__subtitle">
          Track monthly sea ice loss, extent, and related climate indicators.
        </p>
      </header>

      <section className="stats-card">
        <h2 className="stats-card__label">Monthly Change</h2>
        <p className="stats-card__value">-52,000 km²</p>
        <p className="stats-card__meta">vs. January average</p>
      </section>

      <section className="stats-card">
        <h2 className="stats-card__label">Average Ice Thickness</h2>
        <p className="stats-card__value">1.4 m</p>
        <p className="stats-card__meta">Northern Hemisphere</p>
      </section>

      <section className="stats-card">
        <h2 className="stats-card__label">Anomaly</h2>
        <p className="stats-card__value">-8%</p>
        <p className="stats-card__meta">Relative to 1981-2010 baseline</p>
      </section>

      <section className="stats-card">
        <h2 className="stats-card__label">Anomaly</h2>
        <p className="stats-card__value">-8%</p>
        <p className="stats-card__meta">Relative to 1981-2010 baseline</p>
      </section>

      <section className="stats-card">
        <h2 className="stats-card__label">Anomaly</h2>
        <p className="stats-card__value">-8%</p>
        <p className="stats-card__meta">Relative to 1981-2010 baseline</p>
      </section>

      <section className="stats-card">
        <h2 className="stats-card__label">Anomaly</h2>
        <p className="stats-card__value">-8%</p>
        <p className="stats-card__meta">Relative to 1981-2010 baseline</p>
      </section>
    </aside>
  );
};

export default RightStatsPanel;
