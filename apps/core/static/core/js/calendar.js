document.addEventListener("DOMContentLoaded", () => {

    // ================================
    // DOM Elements
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
    // Color Picker
    // ================================
    document.querySelectorAll(".color-dot").forEach(dot => {
        dot.addEventListener("click", () => {
            selectedColor = dot.dataset.color;
            document.querySelectorAll(".color-dot").forEach(d => d.classList.remove("selected"));
            dot.classList.add("selected");
        });
    });


    // ================================
    // FullCalendar
    // ================================
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "dayGridMonth",
        locale: "zh-tw",
        editable: true,
        selectable: true,
        dayMaxEvents: true,

        headerToolbar: {
            left: "prev today next",
            center: "title",
            right: "dayGridMonth,timeGridWeek,timeGridDay",
        },

        events: "/personal/events/",

        eventContent(arg) {
            const pill = document.createElement("div");
            pill.className = "fc-event-pink-pill";
            pill.style.backgroundColor = arg.event.backgroundColor;
            pill.textContent = arg.event.title;

            if (arg.event.extendedProps.is_completed) {
                pill.style.opacity = "0.6";
                pill.style.textDecoration = "line-through";
            }

            return { domNodes: [pill] };
        },

        eventClick(info) {
            currentEvent = info.event;

            modalTitle.textContent = "✏️ 編輯事件";
            eventTitle.value = currentEvent.title;
            eventDate.value = currentEvent.start.toISOString().slice(0, 10);
            eventNote.value = currentEvent.extendedProps.note;
            eventPriority.value = currentEvent.extendedProps.priority;

            selectedColor = currentEvent.extendedProps.true_color;
            document.querySelectorAll(".color-dot").forEach(d =>
                d.classList.toggle("selected", d.dataset.color === selectedColor)
            );

            deleteBtn.classList.remove("hidden");
            modalBg.style.display = "flex";
        },

        dateClick(info) {
            currentEvent = null;

            modalTitle.textContent = "📝 新增事件";
            eventTitle.value = "";
            eventDate.value = info.dateStr;
            eventNote.value = "";
            eventPriority.value = "中";
            selectedColor = "#fda4af";

            document.querySelectorAll(".color-dot").forEach(d =>
                d.classList.toggle("selected", d.dataset.color === selectedColor)
            );

            deleteBtn.classList.add("hidden");
            modalBg.style.display = "flex";
        },

        eventDrop(info) {
            saveUpdatedEvent(info.event);
        },

        eventResize(info) {
            saveUpdatedEvent(info.event);
        },
    });

    calendar.render();


    // ================================
    // Date Picker
    // ================================
    flatpickr("#eventDate", {
        dateFormat: "Y-m-d",
    });


    // ================================
    // API helpers
    // ================================
    function formatDateTime(d) {
        return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,"0")}-${String(d.getDate()).padStart(2,"0")} ` +
               `${String(d.getHours()).padStart(2,"0")}:${String(d.getMinutes()).padStart(2,"0")}`;
    }


    function addEventAPI() {
        fetch("/personal/add/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                title: eventTitle.value,
                start: `${eventDate.value} 09:00`,
                end: `${eventDate.value} 10:00`,
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


    function saveUpdatedEvent(ev) {
        fetch(`/personal/update/${ev.id}/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                title: ev.title,
                start: formatDateTime(ev.start),
                end: formatDateTime(ev.end || ev.start),
                note: ev.extendedProps.note,
                color: ev.extendedProps.true_color,
                priority: ev.extendedProps.priority,
            })
        }).then(() => {
            calendar.refetchEvents();
            loadTasks();
        });
    }


    deleteBtn.onclick = () => {
        if (!currentEvent) return;
        fetch(`/personal/delete/${currentEvent.id}/`, { method: "POST" })
            .then(() => {
                calendar.refetchEvents();
                loadTasks();
                modalBg.style.display = "none";
            });
    };


    saveBtn.onclick = () => {
        if (!eventTitle.value || !eventDate.value) {
            alert("請輸入完整資訊");
            return;
        }

        if (currentEvent) {
            currentEvent.setProp("title", eventTitle.value);
            currentEvent.setExtendedProp("note", eventNote.value);
            currentEvent.setExtendedProp("priority", eventPriority.value);
            currentEvent.setExtendedProp("true_color", selectedColor);
            currentEvent.setStart(`${eventDate.value}T09:00`);
            currentEvent.setEnd(`${eventDate.value}T10:00`);

            saveUpdatedEvent(currentEvent);
            modalBg.style.display = "none";
        } else {
            addEventAPI();
        }
    };


    cancelBtn.onclick = () => modalBg.style.display = "none";
    modalBg.onclick = e => { if (e.target === modalBg) modalBg.style.display = "none"; };


    addEventBtn.onclick = () => {
        currentEvent = null;
        modalTitle.textContent = "📝 新增事件";
        eventTitle.value = "";
        eventDate.value = "";
        eventNote.value = "";
        eventPriority.value = "中";
        selectedColor = "#fda4af";

        document.querySelectorAll(".color-dot").forEach(d =>
            d.classList.toggle("selected", d.dataset.color === selectedColor)
        );

        deleteBtn.classList.add("hidden");
        modalBg.style.display = "flex";
    };


    // ================================
    // 7-day task list
    // ================================
    function loadTasks() {
        fetch("/personal/events/")
            .then(res => res.json())
            .then(events => {
                const now = new Date();
                const seven = new Date(now.getTime() + 7 * 86400 * 1000);

                const filtered = events.filter(e => {
                    if (e.extendedProps.is_completed) return false;
                    const d = new Date(e.start);
                    return d >= now && d <= seven;
                });

                const order = { "高": 1, "中": 2, "低": 3 };
                filtered.sort((a, b) =>
                    order[a.extendedProps.priority] - order[b.extendedProps.priority]
                );

                taskList.innerHTML = filtered.length
                    ? ""
                    : "<p class='opacity-70 italic'>(未來七天沒有任務)</p>";

                filtered.forEach(ev => {
                    const d = new Date(ev.start);
                    const mm = String(d.getMonth()+1).padStart(2,"0");
                    const dd = String(d.getDate()).padStart(2,"0");
                    const weekday = ["週日","週一","週二","週三","週四","週五","週六"][d.getDay()];

                    const row = document.createElement("div");
                    row.className = "task-item flex items-center gap-2 py-1";

                    const checkbox = document.createElement("input");
                    checkbox.type = "checkbox";
                    checkbox.onclick = () => {
                        fetch(`/personal/toggle/${ev.id}/`, { method: "POST" })
                            .then(() => {
                                calendar.refetchEvents();
                                loadTasks();
                            });
                    };

                    const text = document.createElement("span");
                    text.textContent = `${mm}/${dd}（${weekday}）｜${ev.title}`;

                    row.appendChild(checkbox);
                    row.appendChild(text);
                    taskList.appendChild(row);
                });
            });
    }

    loadTasks();
});


