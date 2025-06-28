import React, { useEffect, useState } from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell
} from "recharts";
import { Users, FileText, Building2, ClipboardList, Briefcase, ShieldCheck, Landmark, Banknote } from "lucide-react";

// Paleta Propulsor (do seu cores.json)
const cores = {
  primario: "#267cff",
  secundario: "#263642",
  destaque: "#ffb400",
  alerta: "#e04f5f",
  fundo: "#f5fafd",
  card: "#ffffff",
  texto: "#212529",
  verde: "#12c99b",
  roxo: "#5a31f4"
};

const modulos = [
  { id: "pessoas", label: "Pessoas", icon: <Users size={32} color={cores.primario} /> },
  { id: "contratos", label: "Contratos", icon: <FileText size={32} color={cores.roxo} /> },
  { id: "instituicoes", label: "Instituições", icon: <Building2 size={32} color={cores.primario} /> },
  { id: "requisicoes", label: "Requisições", icon: <ClipboardList size={32} color={cores.destaque} /> },
  { id: "contencioso", label: "Contencioso", icon: <ShieldCheck size={32} color={cores.verde} /> },
  { id: "procuracoes", label: "Procurações", icon: <Landmark size={32} color={cores.primario} /> },
  { id: "depositos", label: "Depósitos", icon: <Banknote size={32} color={cores.destaque} /> },
  { id: "consorcios", label: "Consórcios", icon: <Briefcase size={32} color={cores.alerta} /> },
];

export default function Dashboard() {
  const [dados, setDados] = useState({});
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState("");
  // Simulação de gráfico para demonstrar (substitua por fetch real se quiser)
  const graficoData = [
    { mes: "Jan", Pessoas: 420, Contratos: 320 },
    { mes: "Fev", Pessoas: 390, Contratos: 290 },
    { mes: "Mar", Pessoas: 480, Contratos: 370 },
    { mes: "Abr", Pessoas: 460, Contratos: 350 },
    { mes: "Mai", Pessoas: 500, Contratos: 420 },
    { mes: "Jun", Pessoas: 530, Contratos: 400 }
  ];
  const pieData = [
    { name: "Concluído", value: 75, color: cores.primario },
    { name: "Pendente", value: 25, color: cores.destaque },
  ];

  useEffect(() => {
    // Troque pela sua URL de backend se precisar
    fetch("/api/dashboard/cards")
      .then((resp) => resp.json())
      .then(setDados)
      .catch(() => setErro("Erro ao conectar com API"))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="min-h-screen bg-[#f5fafd] py-8 px-2">
      <div className="max-w-7xl mx-auto">
        {/* Logo Propulsor topo */}
        <div className="flex items-center mb-4">
          <img src="/PropulsorA-Copia.png" alt="Logo Propulsor" className="w-14 h-14 mr-4" />
          <h1 className="text-3xl font-extrabold text-[#267cff] tracking-tight">Painel Propulsor</h1>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          {modulos.map((m) => (
            <div
              key={m.id}
              className="rounded-2xl shadow-md bg-white p-6 flex flex-col items-center border-b-4"
              style={{ borderColor: cores.primario }}
            >
              <div>{m.icon}</div>
              <div className="text-lg font-bold text-[#263642] mt-2">{m.label.toUpperCase()}</div>
              <div className="text-sm text-gray-500">Total:</div>
              <div className="text-3xl font-black mt-1" style={{ color: cores.primario }}>
                {loading ? "..." : dados[m.id] ?? "N/A"}
              </div>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Gráfico de barras */}
          <div className="rounded-2xl shadow-md bg-white p-6">
            <div className="font-bold mb-2">Pessoas vs Contratos (Demo)</div>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={graficoData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="mes" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="Pessoas" fill={cores.primario} radius={[10,10,0,0]} />
                <Bar dataKey="Contratos" fill={cores.destaque} radius={[10,10,0,0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Gráfico pizza objetivo mensal */}
          <div className="rounded-2xl shadow-md bg-white p-6 flex flex-col justify-center items-center">
            <div className="font-bold mb-2">Meta do Mês</div>
            <PieChart width={180} height={180}>
              <Pie
                data={pieData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={70}
                fill={cores.primario}
                label={({ percent }) => `${Math.round(percent * 100)}%`}
              >
                {pieData.map((entry, idx) => (
                  <Cell key={`cell-${idx}`} fill={entry.color} />
                ))}
              </Pie>
            </PieChart>
            <div className="text-2xl font-extrabold mt-2" style={{ color: cores.primario }}>$750 / $1.000</div>
          </div>
          {/* Card visual advisor/ação */}
          <div className="rounded-2xl shadow-md bg-white p-6 flex flex-col justify-between">
            <div className="font-bold mb-2 text-[#5a31f4]">Ação Recomendada</div>
            <div className="mb-4 text-[#263642]">Consulte as movimentações do mês e ajuste o fluxo conforme previsto.</div>
            <button className="bg-[#267cff] text-white rounded-lg px-4 py-2 font-bold shadow transition hover:bg-[#4d99ff]">Ver recomendações</button>
          </div>
        </div>

        {/* Histórico (exemplo) */}
        <div className="mt-8 rounded-2xl shadow-md bg-white p-6">
          <div className="font-bold text-[#267cff] mb-2">Histórico - Cards e Relatórios do CRM</div>
          <div className="text-gray-600 text-sm">Integração automática: todos os cards acima puxam dados em tempo real via API.</div>
        </div>
      </div>
      {erro && <div className="fixed bottom-6 right-6 bg-red-100 text-red-700 px-4 py-2 rounded-xl shadow-xl">{erro}</div>}
    </div>
  );
}
