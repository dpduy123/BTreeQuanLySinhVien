document.addEventListener('DOMContentLoaded', () => {
    fetchData();

    document.getElementById('addForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = document.getElementById('studentId').value;
        const name = document.getElementById('studentName').value;
        const gender = document.getElementById('studentGender').value;

        try {
            const res = await fetch('/api/students', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id, name, gender })
            });
            const result = await res.json();
            if (!res.ok) {
                showNotification(result.error, true);
            } else {
                showNotification("Thêm sinh viên thành công!");
                document.getElementById('addForm').reset();
                fetchData();
            }
        } catch (err) {
            showNotification("Lỗi kết nối", true);
        }
    });

    document.getElementById('searchForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const query = document.getElementById('searchQuery').value.trim();
        if(!query) {
            fetchData();
            return;
        }
        const type = document.getElementById('searchType').value;
        
        fetch(`/api/search?q=${query}&type=${type}`)
            .then(res => res.json())
            .then(data => {
                renderTable(data);
                showNotification(`Tìm thấy ${data.length} kết quả.`);
            });
    });

    document.getElementById('clearSearchBtn').addEventListener('click', () => {
        document.getElementById('searchQuery').value = '';
        fetchData();
    });
});

async function fetchData() {
    try {
        const res = await fetch('/api/data');
        const data = await res.json();
        renderTable(data.table);
        renderTree(data.id_tree, document.getElementById('idBTree'));
        renderTree(data.name_tree, document.getElementById('nameBTree'));
    } catch (err) {
        console.error("Lỗi khi tải dữ liệu", err);
    }
}

function renderTable(tableData) {
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = '';
    if (tableData.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center">Chưa có dữ liệu</td></tr>';
        return;
    }
    tableData.forEach(student => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${student.id}</td>
            <td>${student.name}</td>
            <td>${student.gender}</td>
            <td><button class="btn danger-btn" onclick="deleteStudent('${student.id}')">Xóa</button></td>
        `;
        tbody.appendChild(tr);
    });
}

async function deleteStudent(id) {
    if(!confirm('Bạn có chắc chắn muốn xóa sinh viên này?')) return;
    try {
        const res = await fetch(`/api/students/${id}`, { method: 'DELETE' });
        const result = await res.json();
        if (!res.ok) {
            showNotification(result.error, true);
        } else {
            showNotification("Đã xóa sinh viên.");
            fetchData();
        }
    } catch (err) {
        showNotification("Lỗi kết nối", true);
    }
}

function renderTree(treeData, container) {
    container.innerHTML = '';
    if (!treeData || treeData.keys.length === 0) {
        container.innerHTML = '<p style="color:#94a3b8">Cây trống</p>';
        return;
    }
    const createNodeDOM = (node) => {
        const nodeDiv = document.createElement('div');
        nodeDiv.className = 'btree-node';

        // Keys display
        const keysDiv = document.createElement('div');
        keysDiv.className = 'btree-keys';
        
        node.keys.forEach((k) => {
            if(k === null) return;
            const keyEl = document.createElement('span');
            keyEl.className = 'btree-key';
            keyEl.textContent = String(k);
            keysDiv.appendChild(keyEl);
        });
        nodeDiv.appendChild(keysDiv);

        // Children display
        if (!node.leaf && node.children && node.children.length > 0) {
            const childrenDiv = document.createElement('div');
            childrenDiv.className = 'btree-children';
            
            node.children.forEach(child => {
                const childContainer = document.createElement('div');
                childContainer.className = 'btree-child-container';
                childContainer.appendChild(createNodeDOM(child));
                childrenDiv.appendChild(childContainer);
            });
            nodeDiv.appendChild(childrenDiv);
        }

        return nodeDiv;
    };

    container.appendChild(createNodeDOM(treeData));
}

function showNotification(msg, isError=false) {
    const el = document.getElementById('notification');
    el.textContent = msg;
    el.className = `notification ${isError ? 'error' : ''}`;
    setTimeout(() => {
        el.className = 'notification hidden';
    }, 3000);
}
