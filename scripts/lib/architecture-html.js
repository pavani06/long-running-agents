const escape = value => String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#39;");

export function renderMap(map) {
  const x = component => 48 + component.column * 376;
  const y = component => 64 + component.row * 208;
  const evidence = entries => entries.map(entry => {
    const path = entry.path.split("/").map(encodeURIComponent).join("/");
    return `<a href="${escape(map.repository)}/blob/${map.commit}/${path}#L${entry.start}-L${entry.end}">${escape(entry.path)}:${entry.start}–${entry.end}</a>`;
  }).join("<br>");
  const arrows = map.relations.map(relation => {
    const from = map.components.find(component => component.id === relation.from);
    const to = map.components.find(component => component.id === relation.to);
    const horizontal = from.row === to.row;
    const forward = horizontal ? to.column > from.column : to.row > from.row;
    const x1 = x(from) + (horizontal ? (forward ? 248 : 0) : 124);
    const x2 = x(to) + (horizontal ? (forward ? 0 : 248) : 124);
    const y1 = y(from) + (horizontal ? 48 : (forward ? 96 : 0));
    const y2 = y(to) + (horizontal ? 48 : (forward ? 0 : 96));
    const tx = (x1 + x2) / 2 + (horizontal ? 0 : 16);
    const ty = (y1 + y2) / 2 - (horizontal ? 16 : 0);
    return `<g><title>${escape(relation.description)}</title><path d="M${x1} ${y1} L${x2} ${y2}" stroke="#657080" fill="none" marker-end="url(#arrow)"/>
      <text x="${tx}" y="${ty}" text-anchor="${horizontal ? "middle" : "start"}" class="edge">${escape(relation.label)}</text></g>`;
  }).join("\n");
  const nodes = map.components.map(component => `<a href="#${component.id}">
    <rect x="${x(component)}" y="${y(component)}" width="248" height="96" rx="6" fill="${component.id === map.focus ? "#fff0e6" : "#fafaf8"}" stroke="${component.id === map.focus ? "#bd5128" : "#8a9097"}"/>
    <text x="${x(component) + 16}" y="${y(component) + 28}" class="tag">${String(map.components.indexOf(component) + 1).padStart(2, "0")} / COMPONENTE</text>
    <text x="${x(component) + 16}" y="${y(component) + 60}" class="node">${escape(component.name)}</text>
  </a>`).join("\n");
  return `<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${escape(map.title)}</title><style>
*{box-sizing:border-box}body{margin:0;background:#fafaf8;color:#29323c;font:16px/1.6 system-ui,sans-serif}
main{max-width:1160px;margin:0 auto;padding:48px 24px}h1{font:normal clamp(32px,5vw,52px)/1.1 Georgia,serif;margin:12px 0 24px}
h2{font:normal 28px Georgia,serif;margin-top:48px}.eyebrow,.tag{letter-spacing:.12em;font-size:11px;fill:#657080;color:#657080}
.meta{color:#596473;font-size:14px}.diagram{overflow-x:auto;border-block:1px solid #d5d8da;margin-top:32px}
svg{display:block;width:100%;min-width:850px}.node{font-size:16px;font-weight:600;fill:#29323c}.edge{font:12px system-ui;fill:#596473}
a{color:#265d80;text-underline-offset:3px}a:focus-visible{outline:2px solid #bd5128}section{scroll-margin-top:24px}
.components{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:24px}
.components section{border-top:1px solid #d5d8da;padding-top:12px}h3{font-size:18px;margin:8px 0}code{font-size:13px;overflow-wrap:anywhere}
table{border-collapse:collapse;width:100%;font-size:14px}td,th{text-align:left;vertical-align:top;border-bottom:1px solid #d5d8da;padding:12px 8px}
td:last-child{overflow-wrap:anywhere}footer{border-top:1px solid #d5d8da;margin-top:48px;padding-top:16px;font-size:13px}
@media print{main{padding:0}.diagram{overflow:visible}svg{min-width:0}a{color:inherit}.components section{break-inside:avoid}}
</style></head><body><main><div class="eyebrow">MAPA DO REPOSITÓRIO / VERSÃO 1</div>
<h1>${escape(map.title)}</h1><p>${escape(map.summary)}</p>
<p class="meta">Retrato do commit <a href="${escape(map.repository)}/commit/${map.commit}"><code>${map.commit}</code></a>.<br>
Não é um status ao vivo. O monitor compara este retrato com outro commit; alterações locais ficam fora.</p>
<div class="diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1120 640" role="img" aria-labelledby="map-title map-desc">
<title id="map-title">${escape(map.title)}</title><desc id="map-desc">${escape(map.summary)}. As relações e evidências estão descritas nas tabelas abaixo.</desc>
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#657080"/></marker></defs>
${arrows}${nodes}</svg></div><p class="meta">Selecione um componente para ver responsabilidade, escopo e evidências. Setas representam as relações descritas abaixo.</p>
<h2>Componentes e responsabilidades</h2><div class="components">${map.components.map(component => `<section id="${component.id}"><h3>${escape(component.name)}</h3><p>${escape(component.responsibility)}</p><p><code>${component.paths.map(escape).join(" · ")}</code></p><p class="meta">${evidence(component.evidence)}</p></section>`).join("")}</div>
<h2>Relações verificáveis</h2><table><thead><tr><th>Relação</th><th>Significado</th><th>Evidência no commit</th></tr></thead><tbody>${map.relations.map(relation => `<tr><td>${escape(map.components.find(component => component.id === relation.from).name)} → ${escape(map.components.find(component => component.id === relation.to).name)}</td><td>${escape(relation.description)}</td><td>${evidence(relation.evidence)}</td></tr>`).join("")}</tbody></table>
<h2>Limites da visão geral</h2><ul>${(map.limitations ?? []).map(item => `<li>${escape(item)}</li>`).join("")}</ul>
<footer>Composição própria inspirada no <a href="https://github.com/cathrynlavery/diagram-design/tree/562dbdf93ff3c3da630be4f90f4f6c2548175058">Diagram Design</a>: hierarquia editorial, poucos destaques e conectores ortogonais. Fontes locais; sem dependências de rede para renderizar.</footer>
</main></body></html>\n`;
}
