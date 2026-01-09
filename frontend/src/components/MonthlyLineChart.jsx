import React, { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { getMonthlyAnalytics } from "../api";

export default function MonthlyLineChart() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const analytics = await getMonthlyAnalytics();
        const chartData = Object.entries(analytics)
          .map(([month, amount]) => ({
            month,
            amount: parseFloat(amount.toFixed(2))
          }))
          .sort((a, b) => a.month.localeCompare(b.month));
        setData(chartData);
      } catch (error) {
        console.error("Error fetching analytics:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) return <div className="loading">Loading chart...</div>;
  if (data.length === 0) return <div className="empty-chart">No data available</div>;

  return (
    <div className="chart-container">
      <h3 className="chart-title">📈 Monthly Spending Trend</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip formatter={(value) => `₹${value}`} />
          <Legend />
          <Line type="monotone" dataKey="amount" stroke="#667eea" strokeWidth={2} name="Total Spent" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
