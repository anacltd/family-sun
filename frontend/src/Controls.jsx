import './App.css'

const SunburstControls = ({ generations, setGenerations, palette, setPalette, colorBy, setColorBy }) => {
  return (
    <div className="controls-container">
      <div className="form-group">
        <label htmlFor="generations"># of generations to display:</label>
        <input
          id="generations"
          type="number"
          value={generations}
          onChange={(e) => setGenerations(Number(e.target.value))}
          min="1"
          max="12"
        />
      </div>

      <div className="form-group">
        <label htmlFor="colorBy">Color family tree by:</label>
        <select
          id="colorBy"
          value={colorBy}
          onChange={(e) => setColorBy(e.target.value)}
        >
          <option value="generation">Generation</option>
          <option value="patronym">Patronym</option>
          <option value="department">Department</option>
          <option value="region">Region</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="palette">Color palette:</label>
        <select
          id="palette"
          value={palette}
          onChange={(e) => setPalette(e.target.value)}
        >
          <option value="pastel">Pastel</option>
          <option value="earth">Earth</option>
          <option value="vintage">Vintage</option>
          <option value="soft_rainbow">Soft Rainbow</option>
          <option value="warm">Warm</option>
          <option value="moss">Moss</option>
          <option value="clay">Clay</option>
        </select>
      </div>
    </div>
  );
};

export default SunburstControls;
