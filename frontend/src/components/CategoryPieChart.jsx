import { PieChart, Pie, Tooltip, Legend, ResponsiveContainer } from "recharts";

export default function CategoryPieChart({ data }) {
  if (!data || data.length === 0) {
    return <p className="text-center">No category data</p>;
  }

  return (
    <div className="bg-white p-4 rounded shadow">
      <h3 className="text-lg font-semibold mb-4">Category-wise Expenses</h3>

      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            dataKey="total"
            nameKey="category"
            outerRadius={100}
            fill="#6366f1"
            label
          />
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
