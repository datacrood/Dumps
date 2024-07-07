import dynamic from 'next/dynamic';
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

export default function LineChart({ data, filters }) {
  // Filter and process data based on filters
  const filteredData = data.filter(item => 
    (filters.state === 'All' || item.census_state_name === filters.state) &&
    (filters.district === 'All' || item.census_district_name === filters.district) &&
    (filters.commodity === 'All' || item.commodity_name === filters.commodity)
  );
  console.log(filteredData);
  // Process data for line chart (this is a simplified example)
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const averagePrices = months.map(month => {
    const monthData = filteredData.filter(item => new Date(item.date).getMonth() === months.indexOf(month));
    return monthData.reduce((sum, item) => sum + Number(item.modal_price), 0) / monthData.length || 0;
  });

  return (
    <Plot
      data={[{
        x: months,
        y: averagePrices,
        type: 'scatter',
        mode: 'lines+markers'
      }]}
      layout={{ title: 'Monthly Average Modal Price Trend' }}
    />
  );
}