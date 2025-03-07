"use client";

import { useAppSelector } from "@/src/store/hooks";
import { statsApiSlice } from "@/src/store/services/statsApiSlice";
import NavLink from "@/src/widgets/Header/NavLink/NavLink";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import styles from "./page.module.css";

const Dashboard = () => {
  const router = useRouter();
  const role = useAppSelector((state) => state.user.role);
  useEffect(() => {
    if (role === "student") {
      router.replace("/");
    } else if (role === "mentor") {
      router.replace("mentor");
    }
  }, [role, router]);

  const { data } = statsApiSlice.useGetStatsQuery(null, {
    pollingInterval: 10,
  });

  const barData = [
    {
      name: "Пользователи",
      value: Number(data?.total_students) + Number(data?.total_mentors),
    },
    { name: "Менторы", value: Number(data?.total_mentors) },
    { name: "Ученики", value: Number(data?.total_students) },
  ];

  const pieData = [
    { name: "Принятые заявки", value: Number(data?.accepted) },
    { name: "Отклонённые заявки", value: Number(data?.refused) },
    { name: "В ожидании", value: Number(data?.pending) },
  ];

  const COLORS = ["var(--positive)", "var(--negative)"];

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Страница Администратора</h1>
      <div className={styles.chartContainer}>
        <h2>Общая статистика</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={barData}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--bg-70)" />
            <XAxis dataKey="name" stroke="var(--foreground)" />
            <YAxis stroke="var(--foreground)" />
            <Tooltip
              contentStyle={{
                backgroundColor: "var(--bg-80)",
                border: "none",
                color: "#ffffff", // белый текст при наведении
              }}
            />
            <Legend wrapperStyle={{ color: "#ffffff" }} />
            <Bar dataKey="value" fill="var(--primary)" />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className={styles.chartContainer}>
        <h2>Заявки</h2>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={pieData}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              outerRadius={100}
              fill="var(--primary)"
              label
            >
              {pieData.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={
                    entry.name === "В ожидании"
                      ? "var(--secondary)"
                      : COLORS[index % COLORS.length]
                  }
                />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                backgroundColor: "var(--bg-80)",
                border: "none",
                color: "#ffffff", // белый текст при наведении
              }}
            />
            <Legend wrapperStyle={{ color: "#ffffff" }} />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <NavLink
        asChild
        href="https://prod-team-30-qdrant-mdmsvlv5.final.prodcontest.ru/dashboard"
      >
        Qdrant
      </NavLink>
    </div>
  );
};

export default Dashboard;
