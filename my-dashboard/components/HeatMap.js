import dynamic from 'next/dynamic';
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

export default function HeatMap({ data, filters }) {
  // Filter and process data based on filters
  const filteredData = data.filter(item => 
    (filters.state === 'All' || item.census_state_name === filters.state) &&
    (filters.district === 'All' || item.census_district_name === filters.district) &&
    (filters.commodity === 'All' || item.commodity_name === filters.commodity)
  );
  console.log(filteredData);

  // Process data for heatmap (this is a simplified example)
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const districts = [...new Set(filteredData.map(item => item.census_district_name))];
  const zValues = districts.map(district => 
    months.map(month => {
      const monthData = filteredData.filter(item => 
        item.census_district_name === district && 
        new Date(item.date).getMonth() === months.indexOf(month)
      );
      return monthData.reduce((sum, item) => sum + Number(item.modal_price), 0) / monthData.length || 0;
    })
  );

  return (
    <Plot
      data={[{
        z: zValues,
        x: months,
        y: districts,
        type: 'heatmap',
        colorscale: 'Viridis'
      }]}
      layout={{ title: 'Average Monthly Modal Price Heatmap' }}
    />
  );
}