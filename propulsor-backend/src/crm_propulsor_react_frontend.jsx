import React, { useEffect, useState } from "react";

const LOGO_URL = "/logo-propulsor.png";
const ENDPOINT = "https://api.seusistema.com/crm/metrics";

const MODULOS = [
  { key: "pessoas", label: "Pessoas", color: "#2563eb" },
  { key: "contratos", label: "Contratos", color: "#a855f7" },
  { key: "instituicoes", label: "Instituições", color: "#0891b2" },
  { key: "procuracoes", label: "Procurações", color: "#f43f5e" },
  { key: "depositos", label: "Depósitos", color: "#f59e42" },
  { key: "requisicoes", label: "Requisições", color: "#fbbf24" },
  { key: "contencioso", label: "Contencioso", color: "#38bdf8" },
  { key: "consorcios", label: "Consórcios", color: "#22d3ee" }
];

export default function PainelPropulsorCRM() {
  const [dados, setDados] = useState({});
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");
  const [modulo, setModulo] = useState(MODULOS[0].key);
  const [linhas, setLinhas] = useState([]);

  useEffect(() => {
    async function buscar() {
      setCarregando(true);
      setErro("");
      try {
        const res = await fetch(ENDPOINT);
        const json = await res.json();
        setDados(json);
        setLinhas(json[modulo]?.linhas || []);
      } catch (e) {
        setErro("Erro ao carregar dados");
      }
      setCarregando(false);
    }
    buscar();
  }, [modulo]);

  return (
    <div className="min-h-screen bg-gradient-to-tr from-slate-50 to-blue-100 flex flex-col">
      <header className="px-8 py-6 flex items-center gap-4 bg-white/90 border-b shadow-sm">
        <img src={LOGO_URL} alt="Propulsor logo" className="w-14 h-14 rounded-full bg-white border border-blue-200 shadow" />
        <div>
          <h1 className="text-4xl md:text-5xl font-extrabold text-blue-800 tracking-tight">Propulsor CRM</h1>
          <span className="block text-base font-medium text-blue-600 mt-1">Gestão Jurídica • Contencioso • Comercial</span>
        </div>
      </header>
      <div className="flex-1 flex flex-col lg:flex-row gap-8 p-8 max-w-7xl mx-auto w-full">
        {/* Sidebar */}
        <aside className="lg:w-1/5 w-full flex flex-row lg:flex-col gap-4">
          {MODULOS.map((m) => (
            <button
              key={m.key}
              onClick={() => setModulo(m.key)}
              className={`w-full flex-1 px-4 py-6 rounded-2xl shadow-md border-2 transition-all flex flex-col items-center text-center gap-2 font-bold ${
                modulo === m.key
                  ? `border-[${m.color}] bg-gradient-to-tr from-white via-[${m.color}]/10 to-blue-50 scale-105` : "border-slate-200 bg-white hover:bg-blue-50 hover:border-blue-400"
              }`}
              style={modulo === m.key ? { color: m.color, borderColor: m.color } : { color: "#334155" }}
            >
              <span className="text-2xl md:text-3xl font-black">{dados[m.key]?.total?.toLocaleString("pt-BR") ?? "-"}</span>
              <span className="text-sm uppercase tracking-wider">{m.label}</span>
            </button>
          ))}
        </aside>

        {/* Conteúdo do Módulo */}
        <main className="flex-1 bg-white/80 rounded-3xl shadow-xl p-10 border border-blue-100 flex flex-col">
          <div className="flex items-center gap-2 mb-5">
            <h2 className="text-2xl font-bold capitalize text-blue-800">{MODULOS.find((m) => m.key === modulo)?.label}</h2>
            <span className="ml-2 text-sm text-blue-500 font-medium">({dados[modulo]?.total ?? 0} registros)</span>
          </div>
          {carregando ? (
            <div className="text-blue-600 font-bold text-lg">Carregando...</div>
          ) : erro ? (
            <div className="text-red-500 font-bold">{erro}</div>
          ) : linhas.length === 0 ? (
            <div className="text-gray-500 italic">Nenhum registro encontrado.</div>
          ) : (
            <div className="overflow-x-auto rounded-xl border mt-2">
              <table className="min-w-full text-left border-separate border-spacing-y-1">
                <thead>
                  <tr>
                    {Object.keys(linhas[0]).slice(0,6).map((k) => (
                      <th key={k} className="text-xs text-blue-600 font-bold uppercase px-3 py-1">{k.replace(/_/g," ")}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {linhas.slice(0, 8).map((linha, i) => (
                    <tr key={i} className="hover:bg-blue-50 rounded-xl">
                      {Object.values(linha).slice(0,6).map((val, j) => (
                        <td key={j} className="text-sm px-3 py-1 text-slate-800 whitespace-nowrap">{String(val)}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </main>
      </div>
      <footer className="text-xs text-center text-slate-500 pb-2 pt-8">Propulsor © {new Date().getFullYear()} • Powered by Inteligência Jurídica</footer>
    </div>
  );
}
