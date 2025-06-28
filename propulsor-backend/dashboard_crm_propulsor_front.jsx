// Painel Propulsor - Dashboard CRM (React + Tailwind)
// Design 100% adaptado do exemplo WealthWise, mas com tema Propulsor
// Ícones: lucide-react | Gráficos: recharts
// Cores do Propulsor: #000100, #5001b4, #f7f7f7, #65b1ff, #007dff, #78aadd, #0627ff, #cbcaca, #ffff00

import React, { useEffect, useState } from "react";
import {
  User2,
  FileText,
  Landmark,
  ClipboardList,
  Scales,
  FileSignature,
  PiggyBank,
  CreditCard,
  RocketIcon,
  LogOut,
  LogIn
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from "recharts";

// Paleta Propulsor
const cores = [
  "#000100", // preto absoluto
  "#5001b4", // roxo Propulsor
  "#f7f7f7", // quase branco
  "#65b1ff", // azul claro
  "#007dff", // azul Propulsor
  "#78aadd", // azul intermediário
  "#0627ff", // azul escuro
  "#cbcaca", // cinza claro
  "#ffff00"  // amarelo foguete
];

const CARD_INFOS = [
  { label: "Pessoas", icone: <User2 />, cor: cores[1], modulo: "pessoas" },
  { label: "Contratos", icone: <FileText />, cor: cores[4], modulo: "contratos" },
  { label: "Instituições", icone: <Landmark />, cor: cores[3], modulo: "instituicoes" },
  { label: "Requisições", icone: <ClipboardList />, cor: cores[6], modulo: "requisicoes" },
  { label: "Contencioso", icone: <Scales />, cor: cores[7], modulo: "contencioso" },
  { label: "Procurações", icone: <FileSignature />, cor: cores[1], modulo: "procuracoes" },
  { label: "Depósitos", icone: <PiggyBank />, cor: cores[8], modulo: "depositos" },
  { label: "Consórcios", icone: <CreditCard />, cor: cores[5], modulo: "consorcios" },
];

// Dummy gráfico
const graficoData = [
  { mes: "Jan", Pessoas: 1340, Contratos: 600, Contencioso: 400 },
  { mes: "Fev", Pessoas: 1600, Contratos: 800, Contencioso: 470 },
  { mes: "Mar", Pessoas: 1450, Contratos: 900, Contencioso: 510 },
  { mes: "Abr", Pessoas: 1800, Contratos: 980, Contencioso: 700 },
  { mes: "Mai", Pessoas: 1400, Contratos: 820, Contencioso: 400 },
  { mes: "Jun", Pessoas: 1550, Contratos: 880, Contencioso: 410 },
];

const PieData = [
  { name: "Meta Anual", value: 7000, cor: cores[4] },
  { name: "Realizado", value: 4300, cor: cores[8] },
];

function DashboardPropulsor() {
  const [dados, setDados] = useState({});
  const [loading, setLoading] = useState(true);

  // Busca os dados do backend Flask/Node
  useEffect(() => {
    fetch("/api/dashboard/cards")
      .then((r) => r.json())
      .then((res) => {
        setDados(res);
        setLoading(false);
      });
  }, []);

  return (
    <div className="min-h-screen bg-[#f7f7f7] font-sans">
      {/* Topbar + Logo */}
      <header className="flex items-center px-8 py-4 border-b border-[#cbcaca] bg-white shadow-sm">
        <img src="/PropulsorA-Copia.png" alt="Propulsor" className="h-12 mr-4" />
        <h1 className="text-3xl font-black tracking-tight text-[#5001b4]">Painel Propulsor</h1>
        <span className="ml-auto flex gap-2">
          <Button variant="outline" size="icon" title="Logout"><LogOut /></Button>
        </span>
      </header>

      {/* Cards */}
      <div className="max-w-6xl mx-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mt-8">
        {CARD_INFOS.map((c, i) => (
          <Card
            key={c.label}
            className="p-0 overflow-visible shadow-lg hover:scale-105 transition border-0"
            style={{ borderTop: `5px solid ${c.cor}`, borderRadius: 32 }}
          >
            <CardContent className="flex flex-col items-center justify-center p-6">
              <span className="text-5xl mb-3" style={{ color: c.cor }}>{c.icone}</span>
              <div className="text-lg font-bold text-gray-700 uppercase tracking-widest">{c.label}</div>
              <div className="text-4xl font-extrabold mt-2 mb-1" style={{ color: c.cor }}>
                {loading ? "..." : (dados && dados[c.modulo]) ? dados[c.modulo] : "N/A"}
              </div>
              <div className="text-xs text-gray-400 mt-0">{loading ? "carregando..." : `Tabela: ${c.modulo}`}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Dashboard Secundário */}
      <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6 mt-10">
        {/* Gráfico de Barras */}
        <Card className="lg:col-span-2 p-6 rounded-3xl">
          <div className="text-xl font-bold mb-3 text-[#5001b4]">Cadastros por Mês (Exemplo)</div>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={graficoData}>
              <XAxis dataKey="mes" stroke="#cbcaca" />
              <YAxis stroke="#cbcaca" />
              <Tooltip />
              <Bar dataKey="Pessoas" fill={cores[1]} radius={[8, 8, 0, 0]} />
              <Bar dataKey="Contratos" fill={cores[4]} radius={[8, 8, 0, 0]} />
              <Bar dataKey="Contencioso" fill={cores[6]} radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>
        {/* Gráfico de Pizza */}
        <Card className="p-6 flex flex-col justify-center items-center rounded-3xl">
          <div className="text-xl font-bold mb-2 text-[#5001b4]">Progresso Meta Anual</div>
          <PieChart width={200} height={200}>
            <Pie
              data={PieData}
              cx={100}
              cy={100}
              innerRadius={55}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
              label
            >
              {PieData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.cor} />
              ))}
            </Pie>
          </PieChart>
          <div className="text-3xl font-extrabold mt-2" style={{ color: cores[8] }}>$4.300</div>
          <div className="text-gray-400 text-xs">de $7.000</div>
        </Card>
      </div>

      {/* Rodapé */}
      <footer className="mt-20 py-6 text-center text-sm text-gray-400">Propulsor &copy; {new Date().getFullYear()} - CRM Turbo</footer>
    </div>
  );
}

export default DashboardPropulsor;
