/* ==========================================================
   🌲 Treedoc Version Tree — Bezier 曲線 + 森林動畫版
   ========================================================== */

   function loadVersionTree(docId) {
    fetch(`/treedoc/doc/${docId}/tree/`)
        .then(res => res.json())
        .then(data => renderVersionTree(data));
}

function renderVersionTree(treeData) {
    const container = document.getElementById("versionTree");
    if (!container) return;

    container.innerHTML = ""; // clear

    const svgNS = "http://www.w3.org/2000/svg";
    const svg = document.createElementNS(svgNS, "svg");
    svg.setAttribute("width", "100%");
    svg.setAttribute("height", "700px");
    svg.style.overflow = "visible";

    container.appendChild(svg);

    let ySpacing = 90;
    let xSpacing = 180;

    // 🌿 森林系分支配色
    function branchColor(branch) {
        if (branch === "main") return "#4CAF50";      // 森林綠
        if (branch.startsWith("dev")) return "#8BC34A"; // 嫩草綠
        if (branch.startsWith("feature")) return "#A5D6A7"; // 薄葉綠
        if (branch.startsWith("exp")) return "#81C784";     // 草原綠
        return "#C8E6C9"; // default 淡霧綠
    }

    /* =====================================================
       ✨ 畫 Bezier 曲線（代替直線）
       ===================================================== */
    function drawBezierLine(x1, y1, x2, y2, color) {
        const path = document.createElementNS(svgNS, "path");

        // 控制點位置——做漂亮的彎曲
        const cx1 = x1 + (x2 - x1) * 0.45;
        const cy1 = y1;
        const cx2 = x1 + (x2 - x1) * 0.55;
        const cy2 = y2;

        const d = `M ${x1} ${y1} C ${cx1} ${cy1}, ${cx2} ${cy2}, ${x2} ${y2}`;
        path.setAttribute("d", d);
        path.setAttribute("fill", "none");
        path.setAttribute("stroke", color);
        path.setAttribute("stroke-width", "3");
        path.setAttribute("stroke-linecap", "round");

        // 🌟 pulse 動畫
        path.style.animation = "pulse 2.6s infinite ease-in-out";

        svg.appendChild(path);
    }

    /* =====================================================
       🌳 遞迴繪製版本樹
       ===================================================== */
    function drawNode(node, x, y) {
        // --- 畫連線 (Bezier) ---
        if (node.parentPos) {
            drawBezierLine(
                node.parentPos.x, node.parentPos.y,
                x, y,
                branchColor(node.branch)
            );
        }

        /* --- 畫節點 --- */
        const circle = document.createElementNS(svgNS, "circle");
        circle.setAttribute("cx", x);
        circle.setAttribute("cy", y);
        circle.setAttribute("r", 14);
        circle.setAttribute("fill", branchColor(node.branch));
        circle.setAttribute("stroke", "#ffffffaa");
        circle.setAttribute("stroke-width", 3);
        circle.style.filter = "drop-shadow(0 0 6px rgba(120,180,120,0.5))";
        circle.style.transition = "0.25s";

        // hover 閃光
        circle.addEventListener("mouseenter", () => {
            circle.setAttribute("r", 18);
            circle.style.filter = "drop-shadow(0 0 10px rgba(180,255,180,0.9))";
        });
        circle.addEventListener("mouseleave", () => {
            circle.setAttribute("r", 14);
            circle.style.filter = "drop-shadow(0 0 6px rgba(120,180,120,0.5))";
        });

        svg.appendChild(circle);

        /* --- Label 標籤 --- */
        const label = document.createElementNS(svgNS, "text");
        label.setAttribute("x", x + 22);
        label.setAttribute("y", y + 4);
        label.setAttribute("fill", branchColor(node.branch));
        label.style.fontSize = "14px";
        label.style.fontWeight = "600";
        label.textContent = node.message || "(no message)";
        svg.appendChild(label);

        /* --- 依序畫 children --- */
        node.children.forEach((child, idx) => {
            child.parentPos = { x, y };
            drawNode(child, x + xSpacing, y + idx * ySpacing);
        });
    }

    /* =====================================================
       🌱 根節點（多棵樹時分開擺）
       ===================================================== */
    treeData.forEach((root, index) => {
        drawNode(root, 60, index * 150 + 60);
    });
}

/* =====================================================
   🌟 Pulse 動畫
   ===================================================== */
const style = document.createElement("style");
style.innerHTML = `
@keyframes pulse {
    0%   { stroke-opacity: 0.45; }
    50%  { stroke-opacity: 1; }
    100% { stroke-opacity: 0.45; }
}
`;
document.head.appendChild(style);

