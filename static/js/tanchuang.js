function tanchuang(data) {
        var dialog = new bkDialog({
              type: 'default',
              width: 1000,
              title: data[0].ip + '磁盘占用记录',
              quickClose: true,
              content:'<div class="container-fluid mb0 ">' +
                        '<table id="table1" class="table table-bordered table-striped dataTable no-footer" role="grid" aria-describedby="table2_demo4_info">' +
                        '<thead>\n' +
                  '                        <tr role="row">\n' +
                  '                            <th class="sorting" tabindex="0" aria-controls="table2_demo4" rowspan="1" colspan="1" aria-label="集群: activate to sort column ascending">集群</th>\n' +
                  '                            <th class="sorting" tabindex="0" aria-controls="table2_demo4" rowspan="1" colspan="1" aria-label="ip: activate to sort column ascending">ip</th>\n' +
                  '                            <th class="sorting" tabindex="0" aria-controls="table2_demo4" rowspan="1" colspan="1" aria-label="操作系统: activate to sort column ascending">操作系统</th>\n' +
                  '                            <th class="sorting" tabindex="0" aria-controls="table2_demo4" rowspan="1" colspan="1" aria-label="磁盘分区: activate to sort column ascending">磁盘分区</th>\n' +
                  '                            <th class="sorting" tabindex="0" aria-controls="table2_demo4" rowspan="1" colspan="1" aria-label="录入时间: activate to sort column ascending">录入时间</th>\n' +
                  '                            <th class="sorting" tabindex="0" aria-controls="table2_demo4" rowspan="1" colspan="1" aria-label="已使用: activate to sort column ascending">已使用</th>\n' +
                  '                        </tr>\n' +
                  '                    </thead>' +
                        '</table>' +
                        '</div>'
            });
        dialog.show();

        var language = {
        search: '搜索：',
        lengthMenu: "每页显示 _MENU_ 记录",
        zeroRecords: "没找到相应的数据！",
        info: "分页 _PAGE_ / _PAGES_",
        infoEmpty: "暂无数据！",
        infoFiltered: "(从 _MAX_ 条数据中搜索)",
        paginate: {
            first: '<<',
            last: '>>',
            previous: '上一页',
            next: '下一页',
        }
    };

    $('#table1').dataTable({
        autowidth: false, //适应宽度
        destroy: true,
        paging: true, //隐藏分页
        ordering: false, //关闭排序
        info: false, //隐藏左下角分页信息
        searching: false, //关闭搜索
        lengthChange: false, //不允许用户改变表格每页显示的记录数
        language: language, //汉化
        data: data,
        columns: [
            {"data": "biz"},
            {"data": "ip"},
            {"data": "os"},
            {"data": "diskpath"},
            {"data": "star_time"},
            {"data": "occupy"}
        ]
    })
}