const API_BASE_URL = "http://127.0.0.1:8000/api";

// Active project
const FALLBACK_PROJECT_ID = 1;


/* =========================================================
   PAGE INITIALIZATION
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    initializeWorkspaceListeners();
    fetchActiveWorkspaceRegistry();
    fetchWorkspaceSQLAggregations();
});


/* =========================================================
   EVENT LISTENERS
   ========================================================= */

function initializeWorkspaceListeners() {

    const standardForm = document.getElementById("standard-task-form");
    const aiForm = document.getElementById("ai-quick-add-form");
    const sortBtn = document.getElementById("trigger-sort-btn");
    const refreshBtn = document.getElementById("trigger-refresh-btn");
    const searchInput = document.getElementById("global-search-input");
    const titleInput = document.getElementById("task-title");

    if (standardForm) {
        standardForm.addEventListener("submit", commitStandardTask);
    }

    if (aiForm) {
        aiForm.addEventListener("submit", streamAiQuickAddTask);
    }

    if (sortBtn) {
        sortBtn.addEventListener("click", runWorkspacePrioritySort);
    }

    if (refreshBtn) {
        refreshBtn.addEventListener("click", async () => {
            await fetchActiveWorkspaceRegistry();
            await fetchWorkspaceSQLAggregations();
        });
    }

    if (searchInput) {
        searchInput.addEventListener("input", runRealtimePatternSearch);
    }

    if (titleInput) {
        titleInput.addEventListener("input", () => {
            const errorElement =
                document.getElementById("task-title-error");

            if (titleInput.value.trim() && errorElement) {
                errorElement.textContent = "";
            }
        });
    }
}


/* =========================================================
   GET ALL TASKS
   ========================================================= */

async function fetchActiveWorkspaceRegistry() {

    const listContainer =
        document.getElementById("task-list-container");

    if (!listContainer) return;

    try {

        listContainer.innerHTML =
            '<p class="loading-message">Loading tasks...</p>';

        const response =
            await fetch(`${API_BASE_URL}/tasks/`);

        if (!response.ok) {
            throw new Error(
                `Failed to fetch tasks (${response.status})`
            );
        }

        const tasks = await response.json();

        renderWorkspaceDOMRegistry(tasks);

    } catch (err) {

        console.error("Critical task loading error:", err);

        listContainer.innerHTML = `
            <div class="empty-state">
                Unable to load tasks.<br>
                Make sure FastAPI server is running.
            </div>
        `;
    }
}


/* =========================================================
   PROJECT STATISTICS
   ========================================================= */

async function fetchWorkspaceSQLAggregations() {

    const banner =
        document.getElementById("stats-banner");

    if (!banner) return;

    try {

        const response = await fetch(
            `${API_BASE_URL}/projects/${FALLBACK_PROJECT_ID}/stats`
        );

        if (!response.ok) {
            throw new Error(
                `Stats request failed (${response.status})`
            );
        }

        const stats = await response.json();

        const statusSummary =
            Object.entries(stats.by_status || {})
                .map(
                    ([status, count]) =>
                        `${status}: ${count}`
                )
                .join(" | ");

        banner.textContent =
            `Project Engine Metrics: Total Tasks: ${
                stats.total_tasks ?? 0
            }` +
            (statusSummary
                ? ` | ${statusSummary}`
                : "");

    } catch (err) {

        console.error(
            "Metric dashboard sync failure:",
            err
        );

        banner.textContent =
            "Unable to load project statistics.";
    }
}


/* =========================================================
   RENDER TASKS
   ========================================================= */

function renderWorkspaceDOMRegistry(tasks) {

    const listContainer =
        document.getElementById("task-list-container");

    if (!listContainer) return;

    listContainer.textContent = "";

    if (!Array.isArray(tasks) || tasks.length === 0) {

        const emptyNode =
            document.createElement("div");

        emptyNode.className = "empty-state";
        emptyNode.textContent =
            "No active tasks found.";

        listContainer.appendChild(emptyNode);

        return;
    }


    tasks.forEach((task) => {

        const itemCard =
            document.createElement("div");

        itemCard.className = "task-item-card";


        /* -----------------------------------------
           TASK DETAILS
           ----------------------------------------- */

        const coreDetailsWrapper =
            document.createElement("div");

        coreDetailsWrapper.className =
            "task-core-details";


        const titleHeading =
            document.createElement("h4");

        titleHeading.textContent =
            task.title || "Untitled Task";


        const metaTagsLayout =
            document.createElement("div");

        metaTagsLayout.className =
            "task-meta-tags";


        const priorityBadge =
            document.createElement("span");

        priorityBadge.className =
            `tag tag-priority-${task.priority || "medium"}`;

        priorityBadge.textContent =
            `Priority: ${task.priority || "medium"}`;


        const timelineBadge =
            document.createElement("span");

        timelineBadge.className =
            "tag tag-timeline";

        timelineBadge.textContent =
            `Timeline: ${task.due_date || "Continuous"}`;


        const statusBadge =
            document.createElement("span");

        statusBadge.className =
            "tag tag-status";

        statusBadge.textContent =
            `Status: ${task.status || "todo"}`;


        metaTagsLayout.appendChild(priorityBadge);
        metaTagsLayout.appendChild(timelineBadge);
        metaTagsLayout.appendChild(statusBadge);


        coreDetailsWrapper.appendChild(titleHeading);
        coreDetailsWrapper.appendChild(metaTagsLayout);


        /* -----------------------------------------
           ACTION BUTTONS
           ----------------------------------------- */

        const controlActionsWrapper =
            document.createElement("div");

        controlActionsWrapper.className =
            "task-actions-wrapper";


        /* EDIT / PUT */

        const editBtn =
            document.createElement("button");

        editBtn.type = "button";
        editBtn.textContent = "Edit";
        editBtn.className =
            "task-action-btn btn-edit";

        editBtn.addEventListener("click", () => {

            initiateInlineRecordEdit(
                task,
                itemCard
            );

        });


        /* PATCH */

        const patchBtn =
            document.createElement("button");

        patchBtn.type = "button";
        patchBtn.textContent = "Quick Update";
        patchBtn.className =
            "task-action-btn btn-patch";

        patchBtn.addEventListener("click", () => {

            initiatePatchUpdate(
                task
            );

        });


        /* DELETE */

        const deleteBtn =
            document.createElement("button");

        deleteBtn.type = "button";
        deleteBtn.textContent = "Delete";
        deleteBtn.className =
            "task-action-btn btn-delete";

        deleteBtn.addEventListener(
            "click",
            async () => {

                const confirmed =
                    confirm(
                        `Are you sure you want to delete "${task.title}"?`
                    );

                if (!confirmed) return;

                await executeTargetRecordPurge(
                    task.id
                );
            }
        );


        controlActionsWrapper.appendChild(editBtn);
        controlActionsWrapper.appendChild(patchBtn);
        controlActionsWrapper.appendChild(deleteBtn);


        itemCard.appendChild(coreDetailsWrapper);
        itemCard.appendChild(controlActionsWrapper);

        listContainer.appendChild(itemCard);
    });
}


/* =========================================================
   INLINE EDIT FORM - PUT
   ========================================================= */

function initiateInlineRecordEdit(
    task,
    itemCard
) {

    itemCard.textContent = "";

    const editForm =
        document.createElement("div");

    editForm.className =
        "task-edit-form";


    /* TITLE */

    const titleLabel =
        document.createElement("label");

    titleLabel.textContent =
        "Task Title";


    const titleInput =
        document.createElement("input");

    titleInput.type = "text";
    titleInput.value =
        task.title || "";


    /* PRIORITY */

    const priorityLabel =
        document.createElement("label");

    priorityLabel.textContent =
        "Priority";


    const prioritySelect =
        document.createElement("select");


    ["low", "medium", "high"]
        .forEach((level) => {

            const option =
                document.createElement("option");

            option.value = level;
            option.textContent =
                level.charAt(0).toUpperCase() +
                level.slice(1);

            if (task.priority === level) {
                option.selected = true;
            }

            prioritySelect.appendChild(option);
        });


    /* DUE DATE */

    const dueDateLabel =
        document.createElement("label");

    dueDateLabel.textContent =
        "Timeline";


    const dueDateInput =
        document.createElement("input");

    dueDateInput.type = "text";
    dueDateInput.value =
        task.due_date || "";

    dueDateInput.placeholder =
        "Due date";


    /* STATUS */

    const statusLabel =
        document.createElement("label");

    statusLabel.textContent =
        "Status";


    const statusSelect =
        document.createElement("select");


    ["todo", "in_progress", "done"]
        .forEach((status) => {

            const option =
                document.createElement("option");

            option.value = status;
            option.textContent =
                status.replace("_", " ");

            if (task.status === status) {
                option.selected = true;
            }

            statusSelect.appendChild(option);
        });


    /* ERROR */

    const errorElement =
        document.createElement("span");

    errorElement.className =
        "error-message";


    /* SAVE */

    const saveBtn =
        document.createElement("button");

    saveBtn.type = "button";
    saveBtn.textContent =
        "Save Changes";

    saveBtn.className =
        "task-action-btn btn-edit";


    saveBtn.addEventListener(
        "click",
        async () => {

            const newTitle =
                titleInput.value.trim();

            if (!newTitle) {

                errorElement.textContent =
                    "Title cannot be empty.";

                return;
            }

            errorElement.textContent = "";

            await commitRecordRevision(
                task.id,
                {
                    title: newTitle,
                    priority:
                        prioritySelect.value,
                    due_date:
                        dueDateInput.value.trim() || null,
                    status:
                        statusSelect.value
                }
            );
        }
    );


    /* CANCEL */

    const cancelBtn =
        document.createElement("button");

    cancelBtn.type = "button";
    cancelBtn.textContent =
        "Cancel";

    cancelBtn.className =
        "task-action-btn btn-delete";


    cancelBtn.addEventListener(
        "click",
        () => {
            fetchActiveWorkspaceRegistry();
        }
    );


    editForm.appendChild(titleLabel);
    editForm.appendChild(titleInput);

    editForm.appendChild(priorityLabel);
    editForm.appendChild(prioritySelect);

    editForm.appendChild(dueDateLabel);
    editForm.appendChild(dueDateInput);

    editForm.appendChild(statusLabel);
    editForm.appendChild(statusSelect);

    editForm.appendChild(errorElement);

    const actionRow =
        document.createElement("div");

    actionRow.className =
        "edit-form-actions";

    actionRow.appendChild(saveBtn);
    actionRow.appendChild(cancelBtn);

    editForm.appendChild(actionRow);

    itemCard.appendChild(editForm);
}


/* =========================================================
   PUT - COMPLETE UPDATE
   ========================================================= */

async function commitRecordRevision(
    taskId,
    updates
) {

    try {

        const response =
            await fetch(
                `${API_BASE_URL}/tasks/${taskId}`,
                {
                    method: "PUT",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(updates)
                }
            );


        if (!response.ok) {

            const errorData =
                await response
                    .json()
                    .catch(() => null);

            throw new Error(
                errorData?.detail ||
                `PUT failed (${response.status})`
            );
        }


        await response.json();

        await fetchActiveWorkspaceRegistry();
        await fetchWorkspaceSQLAggregations();


    } catch (err) {

        console.error(
            "Task PUT error:",
            err
        );

        alert(
            `Task update failed: ${err.message}`
        );
    }
}


/* =========================================================
   PATCH - PARTIAL UPDATE
   ========================================================= */

async function initiatePatchUpdate(task) {

    const newPriority =
        prompt(
            `Current priority: ${
                task.priority || "medium"
            }\n\nEnter new priority:\nlow / medium / high`,
            task.priority || "medium"
        );


    if (newPriority === null) {
        return;
    }


    const priority =
        newPriority.trim().toLowerCase();


    if (
        !["low", "medium", "high"]
            .includes(priority)
    ) {

        alert(
            "Invalid priority. Use low, medium or high."
        );

        return;
    }


    try {

        const response =
            await fetch(
                `${API_BASE_URL}/tasks/${task.id}`,
                {
                    method: "PATCH",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        priority: priority
                    })
                }
            );


        if (!response.ok) {

            const errorData =
                await response
                    .json()
                    .catch(() => null);

            throw new Error(
                errorData?.detail ||
                `PATCH failed (${response.status})`
            );
        }


        await response.json();

        await fetchActiveWorkspaceRegistry();
        await fetchWorkspaceSQLAggregations();


    } catch (err) {

        console.error(
            "Task PATCH error:",
            err
        );

        alert(
            `Quick update failed: ${err.message}`
        );
    }
}


/* =========================================================
   POST - CREATE STANDARD TASK
   ========================================================= */

async function commitStandardTask(event) {

    event.preventDefault();


    const titleInput =
        document.getElementById("task-title");

    const titleErrorEl =
        document.getElementById(
            "task-title-error"
        );

    const title =
        titleInput.value.trim();

    const priority =
        document.getElementById(
            "task-priority"
        ).value;

    const due_date =
        document.getElementById(
            "task-duedate"
        ).value.trim();


    if (!title) {

        titleErrorEl.textContent =
            "Task title cannot be empty.";

        return;
    }


    titleErrorEl.textContent = "";


    try {

        const response =
            await fetch(
                `${API_BASE_URL}/tasks/`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        title: title,
                        priority: priority,
                        due_date:
                            due_date || null,
                        project_id:
                            FALLBACK_PROJECT_ID
                    })
                }
            );


        if (!response.ok) {

            const errorData =
                await response
                    .json()
                    .catch(() => null);

            throw new Error(
                errorData?.detail ||
                `Create failed (${response.status})`
            );
        }


        await response.json();

        document
            .getElementById(
                "standard-task-form"
            )
            .reset();


        await fetchActiveWorkspaceRegistry();
        await fetchWorkspaceSQLAggregations();


    } catch (err) {

        console.error(
            "Task creation error:",
            err
        );

        titleErrorEl.textContent =
            err.message;
    }
}


/* =========================================================
   AI QUICK ADD - POST
   ========================================================= */

async function streamAiQuickAddTask(event) {

    event.preventDefault();


    const input =
        document.getElementById(
            "ai-raw-input"
        );

    const description =
        input.value.trim();


    if (!description) {

        alert(
            "Please enter a task description."
        );

        return;
    }


    try {

        const response =
            await fetch(
                `${API_BASE_URL}/tasks/quick-add`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        text: description,
                        project_id:
                            FALLBACK_PROJECT_ID
                    })
                }
            );


        if (!response.ok) {

            const errorData =
                await response
                    .json()
                    .catch(() => null);

            throw new Error(
                errorData?.detail ||
                `AI quick-add failed (${response.status})`
            );
        }


        await response.json();

        document
            .getElementById(
                "ai-quick-add-form"
            )
            .reset();


        await fetchActiveWorkspaceRegistry();
        await fetchWorkspaceSQLAggregations();


    } catch (err) {

        console.error(
            "AI quick-add error:",
            err
        );

        alert(
            `AI task creation failed: ${err.message}`
        );
    }
}


/* =========================================================
   MERGE/INSERTION SORT
   ========================================================= */

async function runWorkspacePrioritySort() {

    try {

        const response =
            await fetch(
                `${API_BASE_URL}/tasks/sorted?project_id=${FALLBACK_PROJECT_ID}`
            );


        if (!response.ok) {

            const errorData =
                await response
                    .json()
                    .catch(() => null);

            throw new Error(
                errorData?.detail ||
                `Sorting failed (${response.status})`
            );
        }


        const sortedTasks =
            await response.json();


        renderWorkspaceDOMRegistry(
            sortedTasks
        );


    } catch (err) {

        console.error(
            "Sorting execution failure:",
            err
        );

        alert(
            `Sorting failed: ${err.message}`
        );
    }
}


/* =========================================================
   REAL-TIME SEARCH
   ========================================================= */

async function runRealtimePatternSearch(event) {

    const query =
        event.target.value.trim();


    if (!query) {

        await fetchActiveWorkspaceRegistry();

        return;
    }


    try {

        const response =
            await fetch(
                `${API_BASE_URL}/tasks/search?q=${encodeURIComponent(query)}`
            );


        if (!response.ok) {

            if (response.status === 404) {

                renderWorkspaceDOMRegistry([]);

                return;
            }

            throw new Error(
                `Search failed (${response.status})`
            );
        }


        const matchedTasks =
            await response.json();


        /*
         * Backend search endpoint returns
         * List[TaskResponse], not a single task.
         */

        renderWorkspaceDOMRegistry(
            matchedTasks
        );


    } catch (err) {

        console.error(
            "Search execution failure:",
            err
        );
    }
}


/* =========================================================
   DELETE TASK
   ========================================================= */

async function executeTargetRecordPurge(
    taskId
) {

    try {

        const response =
            await fetch(
                `${API_BASE_URL}/tasks/${taskId}`,
                {
                    method: "DELETE"
                }
            );


        if (!response.ok) {

            const errorData =
                await response
                    .json()
                    .catch(() => null);

            throw new Error(
                errorData?.detail ||
                `Delete failed (${response.status})`
            );
        }


        await response.json();


        await fetchActiveWorkspaceRegistry();
        await fetchWorkspaceSQLAggregations();


    } catch (err) {

        console.error(
            "Delete task error:",
            err
        );

        alert(
            `Delete failed: ${err.message}`
        );
    }
}