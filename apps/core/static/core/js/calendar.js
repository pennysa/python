document.addEventListener("DOMContentLoaded", function () {

    // ================================
    // 取得 HTML 元素
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
    // 色票選擇
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


        // === 粉色小 pill ===
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

        eventDrop(info) { saveUpdatedEvent(info.event); },
        eventResize(info) { saveUpdatedEvent(info.event); },
    });

    calendar.render();


    // ================================
    // Date Picker
    // ================================
    flatpickr("#eventDate", { dateFormat: "Y-m-d" });


    // ================================
    // 新增事件 API
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
    // 更新事件 API（拖曳或儲存時）
    // ================================
    function saveUpdatedEvent(ev) {
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
    // 刪除事件
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
            // **更新 FullCalendar 事件物件（不會報錯）**
            currentEvent.setProp("title", eventTitle.value);
            currentEvent.setStart(eventDate.value);
            currentEvent.setEnd(eventDate.value);

            currentEvent.setExtendedProp("note", eventNote.value);
            currentEvent.setExtendedProp("priority", eventPriority.value);
            currentEvent.setExtendedProp("true_color", selectedColor);

            saveUpdatedEvent(currentEvent);
            modalBg.style.display = "none";
        } else {
            addEventAPI();
        }
    };


    // ================================
    // Modal 關閉
    // ================================
    cancelBtn.onclick = () => modalBg.style.display = "none";
    modalBg.onclick = e => { if (e.target === modalBg) modalBg.style.display = "none"; };


    // ================================
    // 新增事件按鈕
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
    // 七日任務清單
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

                // 依優先度排序（高 → 中 → 低）
                const order = { "高": 1, "中": 2, "低": 3 };
                filtered.sort((a, b) => order[a.extendedProps.priority] - order[b.extendedProps.priority]);

                taskList.innerHTML = filtered.length
                    ? ""
                    : "<p class='opacity-80 italic'>(未來七天沒有任務 ✨)</p>";

                filtered.forEach(ev => {
                    let row = document.createElement("div");
                    row.className = "task-item flex items-center gap-2 py-1 handwriting";

                    let checkbox = document.createElement("input");
                    checkbox.type = "checkbox";

                    checkbox.onclick = () => {
                        fetch(`/personal/toggle/${ev.id}/`, { method: "POST" }).then(() => {
                            calendar.refetchEvents();
                            loadTasks();
                        });
                    };

                    // ✔ 日期格式成品：01/30（四）
                    let d = new Date(ev.start);
                    let mm = String(d.getMonth() + 1).padStart(2, "0");
                    let dd = String(d.getDate()).padStart(2, "0");
                    let weekday = ["日", "一", "二", "三", "四", "五", "六"][d.getDay()];

                    let text = document.createElement("span");
                    text.textContent = `${mm}/${dd}（${weekday}）｜${ev.title}`;

                    row.appendChild(checkbox);
                    row.appendChild(text);
                    taskList.appendChild(row);
                });
            });
    }

    loadTasks();
});
