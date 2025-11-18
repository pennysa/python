document.addEventListener("DOMContentLoaded", function () {

    // ================================
    // 取得 HTML 元素（與你的 calendar.html 完全相同）
    // ================================
    const calendarEl = document.getElementById("calendar");
    const taskList = document.getElementById("taskList");

    const modalBg = document.getElementById("modal-bg");
    const modalTitle = document.getElementById("modal-title");

    const eventTitle = document.getElementById("eventTitle");
    const eventDate = document.getElementById("eventDate");
    const eventNote = document.getElementById("eventNote");
    const eventPriority = document.getElementById("eventPriority");

    const deleteBtn = document.getElementById("deleteBtn");
    const saveBtn = document.getElementById("saveBtn");
    const cancelBtn = document.getElementById("cancelBtn");
    const addEventBtn = document.getElementById("addEventBtn");

    let selectedColor = "#fda4af";
    let currentEvent = null;


    // ================================
    // 色票選擇（你的 HTML 已支援）
    // ================================
    document.querySelectorAll(".color-dot").forEach(dot => {
        dot.onclick = () => {
            selectedColor = dot.dataset.color;

            document.querySelectorAll(".color-dot")
                .forEach(d => d.classList.remove("selected"));

            dot.classList.add("selected");
        };
    });


    // ================================
    // FullCalendar 初始化
    // ================================
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "dayGridMonth",
        locale: "zh-tw",
        editable: true,
        selectable: true,
        dayMaxEvents: true,
        dayMaxEventRows: true,

        headerToolbar: {
            left: "prev today next",
            center: "title",
            right: "dayGridMonth,timeGridWeek,timeGridDay",
        },

        events: "/personal/events/",


        // === 事件呈現（粉色 pill） ===
        eventContent(arg) {
            let pill = document.createElement("div");
            pill.classList.add("fc-event-pink-pill");

            pill.style.backgroundColor = arg.event.backgroundColor;
            pill.textContent = arg.event.title;

            if (arg.event.extendedProps.is_completed) {
                pill.style.opacity = "0.6";
                pill.style.textDecoration = "line-through";
            }

            return { domNodes: [pill] };
        },


        // === 點事件 → 編輯 ===
        eventClick(info) {
            currentEvent = info.event;

            modalTitle.textContent = "✏️ 編輯事件";

            eventTitle.value = info.event.title;
            eventDate.value = info.event.startStr.slice(0, 10);
            eventNote.value = info.event.extendedProps.note;
            eventPriority.value = info.event.extendedProps.priority;

            selectedColor = info.event.extendedProps.true_color;

            document.querySelectorAll(".color-dot").forEach(d => {
                d.classList.toggle("selected", d.dataset.color === selectedColor);
            });

            deleteBtn.classList.remove("hidden");
            modalBg.style.display = "flex";
        },


        // === 點日期 → 新增 ===
        dateClick(info) {
            currentEvent = null;

            modalTitle.textContent = "📝 新增事件";

            eventTitle.value = "";
            eventDate.value = info.dateStr;
            eventNote.value = "";
            eventPriority.value = "中";

            selectedColor = "#fda4af";

            document.querySelectorAll(".color-dot").forEach(d => {
                d.classList.toggle("selected", d.dataset.color === selectedColor);
            });

            deleteBtn.classList.add("hidden");
            modalBg.style.display = "flex";
        },

        eventDrop(info) { updateEvent(info.event); },
        eventResize(info) { updateEvent(info.event); },
    });

    calendar.render();

    flatpickr("#eventDate", { dateFormat: "Y-m-d" });


    // ================================
    // 新增 API
    // ================================
    function addEventAPI() {
        fetch("/personal/add/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                title: eventTitle.value,
                start: eventDate.value,
                end: eventDate.value,
                note: eventNote.value,
                color: selectedColor,
                priority: eventPriority.value,
            })
        }).then(() => {
            calendar.refetchEvents();
            loadTasks();
            modalBg.style.display = "none";
        });
    }


    // ================================
    // 更新 API
    // ================================
    function updateEvent(ev) {
        fetch(`/personal/update/${ev.id}/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                title: ev.title,
                start: ev.startStr.slice(0, 10),
                end: ev.endStr ? ev.endStr.slice(0, 10) : ev.startStr.slice(0, 10),
                note: ev.extendedProps.note,
                color: ev.extendedProps.true_color,
                priority: ev.extendedProps.priority,
            })
        }).then(() => {
            calendar.refetchEvents();
            loadTasks();
        });
    }


    // ================================
    // 刪除 API
    // ================================
    deleteBtn.onclick = () => {
        if (!currentEvent) return;

        fetch(`/personal/delete/${currentEvent.id}/`, { method: "POST" })
            .then(() => {
                calendar.refetchEvents();
                loadTasks();
                modalBg.style.display = "none";
            });
    };


    // ================================
    // 儲存按鈕（新增 or 更新）
    // ================================
    saveBtn.onclick = () => {
        if (!eventTitle.value || !eventDate.value) {
            alert("請輸入完整資訊");
            return;
        }

        if (currentEvent) {
            updateEvent({
                id: currentEvent.id,
                title: eventTitle.value,
                startStr: eventDate.value,
                endStr: eventDate.value,
                extendedProps: {
                    note: eventNote.value,
                    true_color: selectedColor,
                    priority: eventPriority.value,
                }
            });
            modalBg.style.display = "none";
        } else {
            addEventAPI();
        }
    };


    // ================================
    // Modal 關閉
    // ================================
    cancelBtn.onclick = () => modalBg.style.display = "none";
    modalBg.onclick = (e) => { if (e.target === modalBg) modalBg.style.display = "none"; };


    // ================================
    // 浮動按鈕 → 開啟新增事件
    // ================================
    addEventBtn.onclick = () => {
        currentEvent = null;

        modalTitle.textContent = "📝 新增事件";
        eventTitle.value = "";
        eventDate.value = "";
        eventNote.value = "";
        eventPriority.value = "中";
        selectedColor = "#fda4af";

        document.querySelectorAll(".color-dot").forEach(d => {
            d.classList.toggle("selected", d.dataset.color === selectedColor);
        });

        deleteBtn.classList.add("hidden");
        modalBg.style.display = "flex";
    };


    // ================================
    // 七日任務清單載入
    // ================================
    function loadTasks() {
        fetch("/personal/events/")
            .then(res => res.json())
            .then(events => {
                const now = new Date();
                const seven = new Date(now.getTime() + 7 * 86400 * 1000);

                let filtered = events.filter(e => {
                    if (e.extendedProps.is_completed) return false;
                    let d = new Date(e.start);
                    return d >= now && d <= seven;
                });

                const order = { "高": 1, "中": 2, "低": 3 };
                filtered.sort((a, b) => order[a.extendedProps.priority] - order[b.extendedProps.priority]);

                taskList.innerHTML = filtered.length
                    ? ""
                    : "<p class='opacity-80 italic'>（未來七天沒有任務 ✨）</p>";

                filtered.forEach(ev => {
                    let row = document.createElement("div");
                    row.className = "task-item flex items-center space-x-2 py-1";

                    let checkbox = document.createElement("input");
                    checkbox.type = "checkbox";

                    checkbox.onclick = () => {
                        fetch(`/personal/toggle/${ev.id}/`, { method: "POST" }).then(() => {
                            calendar.refetchEvents();
                            loadTasks();
                        });
                    };

                    let text = document.createElement("span");
                    text.textContent = `${ev.start.slice(5)}｜${ev.title}`;

                    row.appendChild(checkbox);
                    row.appendChild(text);
                    taskList.appendChild(row);
                });
            });
    }

    loadTasks();

});
