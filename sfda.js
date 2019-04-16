var s_resultDataDetail = {};

async function spider_start(pageCount) {
    for (let i = 1; i <= pageCount; i++) {

        let now = new Date();
        let sleepTime = now.getTime() + 1000;
        while (now.getTime() > sleepTime) {
            now = new Date();
        }

        console.log("正在处理第" + i + "页");

        let data = "tableId=36&bcId=152904858822343032639340277073&tableName=TABLE36&viewtitleName=COLUMN361&viewsubTitleName=COLUMN354,COLUMN823,COLUMN356,COLUMN355&tableView=化学药品&cid=0&ytableId=0&searchType=search&COLUMN381=化学药品&curstart=" + i + "&State=1";

        let xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function () {
            if (xmlHttp.readyState === 4 && xmlHttp.status === 200) {
                let listTemp_1 = xmlHttp.responseText.match(/<a href=.*?>.*?<\/p>/gi);

                for (let i = 0; i < listTemp_1.length; i++) {
                    let listTemp_2 = listTemp_1[i].match(/>.*<\/p>/gi)[0];
                    let listTemp_3 = listTemp_2.substring(1, listTemp_2.length - 4);
                    let listTemp_4 = listTemp_1[i].match(/content.jsp.*?null/gi)[0];

                    let xmlHttp_1 = new XMLHttpRequest();
                    xmlHttp_1.onreadystatechange = function () {
                        if (xmlHttp_1.readyState === 4 && xmlHttp_1.status === 200) {
                            let listTemp_5 = xmlHttp_1.responseText.match(/>.+<\/td>[\s\S]*?<\/tr>/gi);
                            let dictTemp = {};

                            for (let i = 0; i < listTemp_5.length - 1; i++) {

                                let listTemp_6 = listTemp_5[i].match(/>.*<\/td>/gi);
                                let listTemp_7;
                                if (listTemp_6[0].length > 6 && listTemp_6[1]) {
                                    listTemp_7 = listTemp_6[0].substring(1, listTemp_6[0].length - 5);

                                    if (listTemp_6[1] <= 6) {
                                        dictTemp[listTemp_7] = '';
                                    }
                                    else {
                                        dictTemp[listTemp_7] = listTemp_6[1].substring(1, listTemp_6[1].length - 5);
                                    }
                                }
                            }

                            s_resultDataDetail[listTemp_3] = dictTemp;
                        }
                    };
                    xmlHttp_1.open("GET", listTemp_4.substring(0, listTemp_4.length - 6));
                    xmlHttp_1.setRequestHeader("Content-Type", "text/html;encoding=gbk");
                    xmlHttp_1.send(null);
                }
            }
        };
        xmlHttp.open("POST", 'search.jsp');
        xmlHttp.setRequestHeader("cache-control", "no-cache");
        xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xmlHttp.send(encodeURI(encodeURI(data)));
    }
}

spider_start(2).then(console.log(s_resultDataDetail));
