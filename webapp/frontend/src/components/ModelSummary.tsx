export default function ModelSummary({ data }: { data: any }) {
  if (!data) return null;

  return (
    <section className="model-card">
      <div>
        <p className="eyebrow">Model Performance</p>
        <h2>{data.best_model}</h2>
        <p>{data.reason}</p>
      </div>

      <div className="model-stats">
        <div>
          <span>Top-K</span>
          <strong>{data.top_k}</strong>
        </div>
        <div>
          <span>RMSE</span>
          <strong>{data.item_based_rmse}</strong>
        </div>
        <div>
          <span>MAE</span>
          <strong>{data.item_based_mae}</strong>
        </div>
      </div>
    </section>
  );
}