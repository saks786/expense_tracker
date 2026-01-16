import { useEffect, useState } from "react";
import CategoryPieChart from "../components/CategoryPieChart";
import MonthlyLineChart from "../components/MonthlyLineChart";
import StatsCards from "../components/StatsCards";

const API_BASE = import.meta.env.VITE_API_BASE_URL;

export default function Dashboard() {
  const [categoryData, setCategoryData] = useState([]);
  const [monthlyData, setMonthlyData] = useState([]);
  const [loading, setLoading] = useState(true);

  const token = localStorage.getItem("token");

  useEffect(() => {
    async function fetchAnalytics() {
      try {
        const headers = {
          Authorization: `Bearer ${token}`,
        };

        const [catRes, monthRes] = await Promise.all([
          fetch(`${API_BASE}/analytics/category`, { headers }),
          fetch(`${API_BASE}/analytics/monthly`, { headers }),
        ]);

        const catData = await catRes.json();
        const monthData = await monthRes.json();

        setCategoryData(catData);
        setMonthlyData(monthData);
      } catch (err) {
        console.error("Failed to load analytics", err);
      } finally {
        setLoading(false);
      }
    }

    fetchAnalytics();
  }, []);

  if (loading) {
    return <p className="text-center mt-10">Loading analytics...</p>;
  }

  return (
    <div className="p-6 space-y-8">
      <StatsCards />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <CategoryPieChart data={categoryData} />
        <MonthlyLineChart data={monthlyData} />
      </div>
    </div>
  );
}
