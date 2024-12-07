import unittest

class TestTrain(unittest.TestCase):
    def setUp(self):
        self.train = train(
            name="Test Train", num=12345, arr_time="10:00", dep_time="18:00",
            src="A", des="B", day_of_travel="Monday", seat_available_in_1AC=10,
            seat_available_in_2AC=20, seat_available_in_SL=30,
            fare_1ac=1000, fare_2ac=500, fare_sl=300
        )
    
    def test_check_availability(self):
        self.assertTrue(self.train.check_availabilty(coach='1AC', ticket_num=5))
        self.assertFalse(self.train.check_availabilty(coach='1AC', ticket_num=15))
    
    def test_book_ticket(self):
        self.train.book_ticket(coach='1AC', no_of_tickets=2)
        self.assertEqual(self.train.seats['1AC'], 8)

class TestTicket(unittest.TestCase):
    def setUp(self):
        self.train = train(name="Test Train", num=12345)
        self.user = user(uid=1001, name="Test User", pwd="testpwd")
        self.ticket = ticket(train=self.train, user=self.user, ticket_num=2, coach="SL")
    
    def test_pnr_generation(self):
        self.assertTrue(self.ticket.pnr.startswith("12345"))
    
    def test_ticket_details(self):
        self.assertEqual(self.ticket.train_num, 12345)
        self.assertEqual(self.ticket.user_name, "Test User")
        self.assertEqual(self.ticket.coach, "SL")
        self.assertEqual(self.ticket.ticket_num, 2)

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = user(uid=1001, name="Test User", pwd="testpwd")
    
    def test_history_update(self):
        test_ticket = ticket(train=None, user=self.user, ticket_num=1, coach="1AC")
        self.assertIn(test_ticket.pnr, self.user.history)

class TestCoreFunctions(unittest.TestCase):
    def setUp(self):
        global trains, users, ticket_dict
        t1 = train('TestTrain', 12345, '10:00', '18:00', 'A', 'B', 'Monday', 10, 10, 10, 1000, 500, 300)
        u1 = user(1001, 'Test User', 'TestCity', '1234567890', 'testpwd')
        trains = {t1.num: t1}
        users = {u1.uid: u1}
        ticket_dict = {}
    
    def test_login_success(self):
        global logged_in, uid
        uid, pwd = 1001, 'testpwd'
        login()
        self.assertTrue(logged_in)
    
    def test_login_failure(self):
        global logged_in, uid
        uid, pwd = 9999, 'wrongpwd'
        with self.assertRaises(Exception):
            login()
        self.assertFalse(logged_in)
    
    def test_booking_ticket(self):
        global logged_in, uid
        logged_in, uid = True, 1001
        trains[12345].seats['1AC'] = 5
        book_ticket()
        self.assertEqual(trains[12345].seats['1AC'], 3)  # Assuming 2 tickets booked
    
    def test_cancel_ticket(self):
        global logged_in, uid, ticket_dict
        logged_in, uid = True, 1001
        tick = ticket(trains[12345], users[1001], 2, '1AC')
        ticket_dict[tick.pnr] = tick
        trains[12345].seats['1AC'] = 3
        cancel_ticket()
        self.assertEqual(trains[12345].seats['1AC'], 5)

if __name__ == '__main__':
    unittest.main()
