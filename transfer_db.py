import sqlite3

con = sqlite3.connect("main_db.s3db")
cur = con.cursor()

con2 = sqlite3.connect("db.sqlite3")
cur2 = con2.cursor()

res = cur.execute("SELECT * FROM tests_info")

question_id = 0
answer_id = 1

data = []

for r in res:
    data.append(r[1])


for d in data:

    content = cur.execute(f"SELECT * FROM '{d}'")

    title_id = cur2.execute(f"SELECT id FROM EduTest_topic WHERE title = '{d.lower()}'").fetchone()[0]
    print(f'Тема: {d}, id: {title_id}' + '\n')

    for row in content:
        answer1 = None
        answer2 = None
        answer3 = None
        answer4 = None
        answer5 = None
        answer6 = None

        question_id += 1
        question = (question_id, row[1], row[2], title_id)
        print(question)
        print("")

        cur2.execute(f"INSERT INTO EduTest_question (id, question_text, img_ref, topic_id_id) VALUES (?, ?, ?, ?)", question)

        if int(row[15]) == 1:
            answer = (answer_id, row[3], row[9], True, question_id)
        else:
            answer = (answer_id, row[3], row[9], False, question_id)
        answer_id += 1

        if int(row[15]) == 2:
            answer2 = (answer_id, row[4], row[10], True, question_id)
        else:
            answer2 = (answer_id, row[4], row[10], False, question_id)
        answer_id += 1

        if int(row[15]) == 3:
            answer3 = (answer_id, row[5], row[11], True, question_id)
        else:
            answer3 = (answer_id, row[5], row[11], False, question_id)
        answer_id += 1

        if row[6] != 'NULL' or row[12] != 'NULL':
            if int(row[15]) == 4:
                answer4 = (answer_id, row[6], row[12], True, question_id)
            else:
                answer4 = (answer_id, row[6], row[12], False, question_id)
            answer_id += 1

        if row[7] != 'NULL' or row[13] != 'NULL':
            if int(row[15]) == 5:
                answer5 = (answer_id, row[7], row[13], True, question_id)
            else:
                answer5 = (answer_id, row[7], row[13], False, question_id)
            answer_id += 1

        if row[8] != 'NULL' or row[14] != 'NULL':
            if int(row[15]) == 6:
                answer6 = (answer_id, row[8], row[14], True, question_id)
            else:
                answer6 = (answer_id, row[8], row[14], False, question_id)
            answer_id += 1

        print(answer)
        cur2.execute("INSERT INTO EduTest_answer (id, answer_text, img_ref, is_correct, question_id_id) VALUES (?, ?, ?, ?, ?)", answer)
        print(answer2)
        cur2.execute("INSERT INTO EduTest_answer (id, answer_text, img_ref, is_correct, question_id_id) VALUES (?, ?, ?, ?, ?)", answer2)
        print(answer3)
        cur2.execute(
            "INSERT INTO EduTest_answer (id, answer_text, img_ref, is_correct, question_id_id) VALUES (?, ?, ?, ?, ?)",
            answer3)
        if answer4:
            print(answer4)
            cur2.execute(
                "INSERT INTO EduTest_answer (id, answer_text, img_ref, is_correct, question_id_id) VALUES (?, ?, ?, ?, ?)",
                answer4)
        if answer5:
            print(answer5)
            cur2.execute(
                "INSERT INTO EduTest_answer (id, answer_text, img_ref, is_correct, question_id_id) VALUES (?, ?, ?, ?, ?)",
                answer5)
        if answer6:
            print(answer6)
            cur2.execute(
                "INSERT INTO EduTest_answer (id, answer_text, img_ref, is_correct, question_id_id) VALUES (?, ?, ?, ?, ?)",
                answer6)
        print("")

    print("=====================")

# print(title_id.fetchone()[0])
con2.commit()
