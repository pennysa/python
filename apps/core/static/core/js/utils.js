/**
 * Planora 全站通用 AJAX 函數
 * 使用 fetch + 自動加入 CSRF Token + JSON/文字自動解析
 */

async function sendRequest({
    url,
    method = "GET",
    params = null,
    data = null,
    onSuccess = () => {},
    onError = null,
    onComplete = null,
}) {

    if (!url) {
        console.error("❌ sendRequest：缺少 URL");
        return;
    }

    method = method.toUpperCase();

    // ======= 處理 URL query string =======
    if (params && typeof params === "object") {
        const query = new URLSearchParams(params).toString();
        url += (url.includes("?") ? "&" : "?") + query;
    }

    const headers = {
        Accept: "application/json",
    };

    let body = null;

    // ======= 取得 CSRF Token =======
    const csrfToken = document.querySelector(
        'input[name="csrfmiddlewaretoken"]'
    )?.value;

    // ======= 處理 POST / PATCH / DELETE 的資料 =======
    if (data && method !== "GET") {
        const isFormData = data instanceof FormData;

        if (isFormData) {
            // FormData 時瀏覽器自動設定 Content-Type
            if (csrfToken && !data.has("csrfmiddlewaretoken")) {
                data.append("csrfmiddlewaretoken", csrfToken);
            }
            body = data;
        } else {
            headers["Content-Type"] = "application/json";
            if (csrfToken) headers["X-CSRFToken"] = csrfToken;
            body = JSON.stringify(data);
        }
    }

    try {
        // ======= 發送 AJAX =======
        const response = await fetch(url, {
            method,
            headers,
            body,
        });

        // 錯誤處理（HTTP 4xx / 5xx）
        if (!response.ok) {
            const contentType = response.headers.get("Content-Type");
            const errorData =
                contentType && contentType.includes("application/json")
                    ? await response.json()
                    : await response.text();

            throw typeof errorData === "string"
                ? { message: errorData }
                : errorData;
        }

        // ======= 回傳資料：依 Content-Type 自動解析 =======
        const contentType = response.headers.get("Content-Type");
        const responseData =
            contentType && contentType.includes("application/json")
                ? await response.json()
                : await response.text();

        onSuccess(responseData);

    } catch (error) {
        console.error("❌ AJAX Request failed:", error);

        const msg = error.message || "請求失敗，請稍後再試";

        if (typeof onError === "function") {
            onError(error);
        } else {
            alert(msg);
        }

    } finally {
        if (typeof onComplete === "function") onComplete();
    }
}
