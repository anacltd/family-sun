import Plot from 'react-plotly.js';
import { useRef, useEffect } from 'react';
import './ChartArea.css';

const palettes = {
  earth: ["#8c510a", "#bf812d", "#dfc27d", "#f6e8c3", "#c7eae5", "#80cdc1", "#35978f", "#01665e", "#003c30", "#d9f0d3", "#ccebc5", "#a8ddb5", "#7bccc4", "#4eb3d3", "#2b8cbe", "#0868ac", "#084081", "#fddbc7", "#f4a582", "#d6604d"],
  vintage: ["#cdb79e", "#f0e68c", "#deb887", "#d2b48c", "#f5deb3", "#a0522d", "#cd853f", "#8b4513", "#bc8f8f", "#e9967a", "#dda0dd", "#f08080", "#e6e6fa", "#b0c4de", "#4682b4", "#708090", "#778899", "#a9a9a9", "#c0c0c0", "#d3d3d3"],
  soft_rainbow: ["#fde0dd", "#fa9fb5", "#f768a1", "#dd3497", "#ae017e", "#7a0177", "#49006a", "#e0ecf4", "#bfd3e6", "#9ebcda", "#8c96c6", "#8c6bb1", "#88419d", "#810f7c", "#4d004b", "#fef0d9", "#fdcc8a", "#fc8d59", "#e34a33", "#b30000"],
  warm: ["#8c4b35", "#a65e3f", "#bf7643", "#d9a066", "#eec27a", "#f4db9d", "#ebd9b4", "#c7ba9d", "#a69a84", "#7b6651", "#4e3926", "#9b7653", "#b3926a", "#d0b484", "#e3c97e", "#c6a664", "#9a8253", "#6f5c3a", "#4a3d2b", "#33291d"],
  moss: ["#5b5f41", "#6a8a62", "#91b77c", "#a7c796", "#d4e8c4", "#d9c7a1", "#c49d6e", "#926e43", "#694f2d", "#4b3b23", "#3d2e1e", "#7b775f", "#8fa68e", "#bacca9", "#cedbb7", "#b28d5c", "#986c43", "#795436", "#5f402e", "#3a2a1e"],
  clay: ["#7c665b", "#927e6b", "#b19b88", "#d1c4a9", "#e7e0c7", "#bcaaa4", "#a1887f", "#8d6e63", "#6d4c41", "#4e342e", "#3e2723", "#cdb79e", "#b79f8f", "#a38c7b", "#8d7969", "#7b6859", "#6a574a", "#58453b", "#47352d", "#36251f"]
};

function ChartArea({ chartData, palette, isSidebarOpen, setPlotlyNodeReference }) {
  const plotComponentRef = useRef(null);

  useEffect(() => {
    if (plotComponentRef.current && plotComponentRef.current.el) {
      setPlotlyNodeReference(plotComponentRef.current.el);
    } else {
      setPlotlyNodeReference(null);
    }

    return () => {
      if (plotComponentRef.current && plotComponentRef.current.el) {
        setPlotlyNodeReference(null);
      }
    };
  }, [chartData, setPlotlyNodeReference]);

  return (
    <div className={`chart-area ${isSidebarOpen ? 'sidebar-open' : 'sidebar-closed'}`}>
      {chartData && (
        <div className="chart-container" id="family-tree">
          <Plot
            ref={plotComponentRef}
            data={chartData}
            layout={{
              margin: { l: 0, r: 0, b: 0, t: 40 },
              title: chartData.title || 'Family Tree Sunburst',
              sunburstcolorway: palettes[palette],
              paper_bgcolor: 'rgba(0,0,0,0)',
              plot_bgcolor: 'rgba(0,0,0,0)',
            }}
            useResizeHandler={true}
            style={{ width: '100%', height: '100%' }}
            config={{
                displaylogo: false,
                modeBarButtonsToRemove: ['toImage']
            }}
          />
        </div>
      )}
    </div>
  );
}

export default ChartArea;