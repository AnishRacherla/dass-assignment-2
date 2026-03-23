# QuickCart Black-Box Passing Tests Report

### Passing Test 1: Missing Roll Number
- **Endpoint tested**: GET /api/v1/products
- **Request payload**:
  - Method: GET
  - URL: http://localhost:8080/api/v1/products
  - Headers: None
  - Body: None
- **Expected result**: 401 HTTP Status Code
- **Actual result observed**: 401 HTTP Status Code
- **Reason why this test case is useful**: Validates that missing roll number is processed correctly according to specification, preventing regressions.

### Passing Test 2: Invalid Roll Number
- **Endpoint tested**: GET /api/v1/products
- **Request payload**:
  - Method: GET
  - URL: http://localhost:8080/api/v1/products
  - Headers: {'X-Roll-Number': 'abc', 'X-User-ID': '1'}
  - Body: None
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that invalid roll number is processed correctly according to specification, preventing regressions.

### Passing Test 3: Missing User Id
- **Endpoint tested**: GET /api/v1/cart
- **Request payload**:
  - Method: GET
  - URL: http://localhost:8080/api/v1/cart
  - Headers: {'X-Roll-Number': '123'}
  - Body: None
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that missing user id is processed correctly according to specification, preventing regressions.

### Passing Test 4: Add To Cart Missing All Headers
- **Endpoint tested**: POST /api/v1/cart/add
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/cart/add
  - Headers: None
  - Body: {'product_id': 1, 'quantity': 1}
- **Expected result**: 401 HTTP Status Code
- **Actual result observed**: 401 HTTP Status Code
- **Reason why this test case is useful**: Validates that add to cart missing all headers is processed correctly according to specification, preventing regressions.

### Passing Test 5: Get Products Structure
- **Endpoint tested**: GET /api/v1/products
- **Request payload**:
  - Method: GET
  - URL: http://localhost:8080/api/v1/products
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: None
- **Expected result**: 200 HTTP Status Code
- **Actual result observed**: 200 HTTP Status Code
- **Reason why this test case is useful**: Validates that get products structure is processed correctly according to specification, preventing regressions.

### Passing Test 6: Get Products Full Schema For All Items
- **Endpoint tested**: GET /api/v1/products
- **Request payload**:
  - Method: GET
  - URL: http://localhost:8080/api/v1/products
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: None
- **Expected result**: 200 HTTP Status Code
- **Actual result observed**: 200 HTTP Status Code
- **Reason why this test case is useful**: Validates that get products full schema for all items is processed correctly according to specification, preventing regressions.

### Passing Test 7: Invalid Product Id
- **Endpoint tested**: GET /api/v1/products/999999
- **Request payload**:
  - Method: GET
  - URL: http://localhost:8080/api/v1/products/999999
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: None
- **Expected result**: 404 HTTP Status Code
- **Actual result observed**: 404 HTTP Status Code
- **Reason why this test case is useful**: Validates that invalid product id is processed correctly according to specification, preventing regressions.

### Passing Test 8: Product Detail Matches List Entry
- **Endpoint tested**: GET /api/v1/products/1
- **Request payload**:
  - Method: GET
  - URL: http://localhost:8080/api/v1/products/1
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: None
- **Expected result**: 200 HTTP Status Code
- **Actual result observed**: 200 HTTP Status Code
- **Reason why this test case is useful**: Validates that product detail matches list entry is processed correctly according to specification, preventing regressions.

### Passing Test 9: Add To Cart Valid
- **Endpoint tested**: POST /api/v1/cart/add
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/cart/add
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'product_id': 1, 'quantity': 2}
- **Expected result**: 200 HTTP Status Code
- **Actual result observed**: 200 HTTP Status Code
- **Reason why this test case is useful**: Validates that add to cart valid is processed correctly according to specification, preventing regressions.

### Passing Test 10: Add To Cart Negative Quantity
- **Endpoint tested**: POST /api/v1/cart/add
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/cart/add
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'product_id': 1, 'quantity': -5}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that add to cart negative quantity is processed correctly according to specification, preventing regressions.

### Passing Test 11: Add To Cart Invalid Product
- **Endpoint tested**: POST /api/v1/cart/add
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/cart/add
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'product_id': 999999, 'quantity': 1}
- **Expected result**: 404 HTTP Status Code
- **Actual result observed**: 404 HTTP Status Code
- **Reason why this test case is useful**: Validates that add to cart invalid product is processed correctly according to specification, preventing regressions.

### Passing Test 12: Add To Cart Exceed Stock
- **Endpoint tested**: POST /api/v1/cart/add
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/cart/add
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'product_id': 1, 'quantity': 100000}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that add to cart exceed stock is processed correctly according to specification, preventing regressions.

### Passing Test 13: Cart Structure
- **Endpoint tested**: GET /api/v1/cart
- **Request payload**:
  - Method: GET
  - URL: http://localhost:8080/api/v1/cart
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: None
- **Expected result**: 200 HTTP Status Code
- **Actual result observed**: 200 HTTP Status Code
- **Reason why this test case is useful**: Validates that cart structure is processed correctly according to specification, preventing regressions.

### Passing Test 14: Cart Items Have Required Fields After Add
- **Endpoint tested**: GET /api/v1/cart
- **Request payload**:
  - Method: GET
  - URL: http://localhost:8080/api/v1/cart
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: None
- **Expected result**: 200 HTTP Status Code
- **Actual result observed**: 200 HTTP Status Code
- **Reason why this test case is useful**: Validates that cart items have required fields after add is processed correctly according to specification, preventing regressions.

### Passing Test 15: Cart Total Never Negative
- **Endpoint tested**: GET /api/v1/cart
- **Request payload**:
  - Method: GET
  - URL: http://localhost:8080/api/v1/cart
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: None
- **Expected result**: 200 HTTP Status Code
- **Actual result observed**: 200 HTTP Status Code
- **Reason why this test case is useful**: Validates that cart total never negative is processed correctly according to specification, preventing regressions.

### Passing Test 16: Cart Isolated Between Users
- **Endpoint tested**: GET /api/v1/cart
- **Request payload**:
  - Method: GET
  - URL: http://localhost:8080/api/v1/cart
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '3'}
  - Body: None
- **Expected result**: 200 HTTP Status Code
- **Actual result observed**: 200 HTTP Status Code
- **Reason why this test case is useful**: Validates that cart isolated between users is processed correctly according to specification, preventing regressions.

### Passing Test 17: Apply Invalid Coupon
- **Endpoint tested**: POST /api/v1/coupon/apply
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/coupon/apply
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'code': 'INVALID'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that apply invalid coupon is processed correctly according to specification, preventing regressions.

### Passing Test 18: Apply Coupon Empty Body
- **Endpoint tested**: POST /api/v1/coupon/apply
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/coupon/apply
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: None
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that apply coupon empty body is processed correctly according to specification, preventing regressions.

### Passing Test 19: Apply Coupon Empty String Code
- **Endpoint tested**: POST /api/v1/coupon/apply
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/coupon/apply
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'code': ''}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that apply coupon empty string code is processed correctly according to specification, preventing regressions.

### Passing Test 20: Checkout Invalid Payment
- **Endpoint tested**: POST /api/v1/checkout
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/checkout
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'payment_method': 'UPI'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that checkout invalid payment is processed correctly according to specification, preventing regressions.

### Passing Test 21: Checkout No Body
- **Endpoint tested**: POST /api/v1/checkout
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/checkout
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: None
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that checkout no body is processed correctly according to specification, preventing regressions.

### Passing Test 22: Wallet Add Invalid Amount
- **Endpoint tested**: POST /api/v1/wallet/add
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/wallet/add
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'amount': 0}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that wallet add invalid amount is processed correctly according to specification, preventing regressions.

### Passing Test 23: Wallet Pay Insufficient Balance
- **Endpoint tested**: POST /api/v1/wallet/pay
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/wallet/pay
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'amount': 100000}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that wallet pay insufficient balance is processed correctly according to specification, preventing regressions.

### Passing Test 24: Wallet Add Missing Roll Number
- **Endpoint tested**: POST /api/v1/wallet/add
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/wallet/add
  - Headers: None
  - Body: {'amount': 100}
- **Expected result**: 401 HTTP Status Code
- **Actual result observed**: 401 HTTP Status Code
- **Reason why this test case is useful**: Validates that wallet add missing roll number is processed correctly according to specification, preventing regressions.

### Passing Test 25: Wallet Add Missing User Id
- **Endpoint tested**: POST /api/v1/wallet/add
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/wallet/add
  - Headers: {'X-Roll-Number': '123'}
  - Body: {'amount': 100}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that wallet add missing user id is processed correctly according to specification, preventing regressions.

### Passing Test 26: Wallet Add String Amount
- **Endpoint tested**: POST /api/v1/wallet/add
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/wallet/add
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'amount': '100'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that wallet add string amount is processed correctly according to specification, preventing regressions.

### Passing Test 27: Review Invalid Rating
- **Endpoint tested**: POST /api/v1/products/1/reviews
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/products/1/reviews
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'rating': 10, 'comment': 'Bad'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that review invalid rating is processed correctly according to specification, preventing regressions.

### Passing Test 28: Ticket Invalid Subject
- **Endpoint tested**: POST /api/v1/support/ticket
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/support/ticket
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'subject': 'Hi', 'message': 'Help me'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that ticket invalid subject is processed correctly according to specification, preventing regressions.

### Passing Test 29: Add To Cart Non Integer Quantity
- **Endpoint tested**: POST /api/v1/cart/add
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/cart/add
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'product_id': 1, 'quantity': 'two'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that add to cart non integer quantity is processed correctly according to specification, preventing regressions.

### Passing Test 30: Coupon Missing Code Field
- **Endpoint tested**: POST /api/v1/coupon/apply
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/coupon/apply
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: None
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that coupon missing code field is processed correctly according to specification, preventing regressions.

### Passing Test 31: Wallet Add Negative Amount
- **Endpoint tested**: POST /api/v1/wallet/add
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/wallet/add
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'amount': -50}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that wallet add negative amount is processed correctly according to specification, preventing regressions.

### Passing Test 32: Wallet Add Missing Amount Field
- **Endpoint tested**: POST /api/v1/wallet/add
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/wallet/add
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: None
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that wallet add missing amount field is processed correctly according to specification, preventing regressions.

### Passing Test 33: Wallet Pay Missing Amount Field
- **Endpoint tested**: POST /api/v1/wallet/pay
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/wallet/pay
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: None
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that wallet pay missing amount field is processed correctly according to specification, preventing regressions.

### Passing Test 34: Wallet Pay Negative Amount
- **Endpoint tested**: POST /api/v1/wallet/pay
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/wallet/pay
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'amount': -10}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that wallet pay negative amount is processed correctly according to specification, preventing regressions.

### Passing Test 35: Review Missing Rating
- **Endpoint tested**: POST /api/v1/products/1/reviews
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/products/1/reviews
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'comment': 'Nice product'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that review missing rating is processed correctly according to specification, preventing regressions.

### Passing Test 36: Review Missing Comment Field
- **Endpoint tested**: POST /api/v1/products/1/reviews
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/products/1/reviews
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'rating': 4}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that review missing comment field is processed correctly according to specification, preventing regressions.

### Passing Test 37: Ticket Missing Message Field
- **Endpoint tested**: POST /api/v1/support/ticket
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/support/ticket
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'subject': 'Order issue'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that ticket missing message field is processed correctly according to specification, preventing regressions.

### Passing Test 38: Add To Cart Float Quantity
- **Endpoint tested**: POST /api/v1/cart/add
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/cart/add
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'product_id': 1, 'quantity': 1.5}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that add to cart float quantity is processed correctly according to specification, preventing regressions.

### Passing Test 39: Checkout Missing Payment Method Field
- **Endpoint tested**: POST /api/v1/checkout
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/checkout
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: None
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that checkout missing payment method field is processed correctly according to specification, preventing regressions.

### Passing Test 40: Checkout Non Json Body
- **Endpoint tested**: POST /api/v1/checkout
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/checkout
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: not-json
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that checkout non json body is processed correctly according to specification, preventing regressions.

### Passing Test 41: Review Non Integer Rating
- **Endpoint tested**: POST /api/v1/products/1/reviews
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/products/1/reviews
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'rating': 'five', 'comment': 'Text rating'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that review non integer rating is processed correctly according to specification, preventing regressions.

### Passing Test 42: Support Ticket Valid Payload Creates Ticket
- **Endpoint tested**: POST /api/v1/support/ticket
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/support/ticket
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'subject': 'Order #12345 delayed delivery', 'message': 'My order is delayed by more than 3 days. Please help.'}
- **Expected result**: 200 HTTP Status Code
- **Actual result observed**: 200 HTTP Status Code
- **Reason why this test case is useful**: Validates that support ticket valid payload creates ticket is processed correctly according to specification, preventing regressions.

### Passing Test 43: Profile Update Short Name
- **Endpoint tested**: PUT /api/v1/profile
- **Request payload**:
  - Method: PUT
  - URL: http://localhost:8080/api/v1/profile
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'name': 'A', 'phone': '1234567890'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that profile update short name is processed correctly according to specification, preventing regressions.

### Passing Test 44: Profile Update Invalid Phone
- **Endpoint tested**: PUT /api/v1/profile
- **Request payload**:
  - Method: PUT
  - URL: http://localhost:8080/api/v1/profile
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'name': 'Valid Name', 'phone': '123456789'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that profile update invalid phone is processed correctly according to specification, preventing regressions.

### Passing Test 45: Profile Update Valid
- **Endpoint tested**: PUT /api/v1/profile
- **Request payload**:
  - Method: PUT
  - URL: http://localhost:8080/api/v1/profile
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'name': 'John Doe', 'phone': '1234567890'}
- **Expected result**: 200 HTTP Status Code
- **Actual result observed**: 200 HTTP Status Code
- **Reason why this test case is useful**: Validates that profile update valid is processed correctly according to specification, preventing regressions.

### Passing Test 46: Address Add Invalid Label
- **Endpoint tested**: POST /api/v1/addresses
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/addresses
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'label': 'INVALID_LABEL', 'street': '123 Main St', 'city': 'Metropolis', 'pincode': '123456'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that address add invalid label is processed correctly according to specification, preventing regressions.

### Passing Test 47: Address Add Short Street
- **Endpoint tested**: POST /api/v1/addresses
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/addresses
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'label': 'HOME', 'street': '123', 'city': 'Metropolis', 'pincode': '123456'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that address add short street is processed correctly according to specification, preventing regressions.

### Passing Test 48: Address Add Invalid Pincode
- **Endpoint tested**: POST /api/v1/addresses
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/addresses
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'label': 'HOME', 'street': '123 Main St', 'city': 'Metropole', 'pincode': '12345'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that address add invalid pincode is processed correctly according to specification, preventing regressions.

### Passing Test 49: Address Update Illegal Field City
- **Endpoint tested**: PUT /api/v1/addresses/1
- **Request payload**:
  - Method: PUT
  - URL: http://localhost:8080/api/v1/addresses/1
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'city': 'New City', 'street': 'Brand New Street'}
- **Expected result**: 200 HTTP Status Code
- **Actual result observed**: 200 HTTP Status Code
- **Reason why this test case is useful**: Validates that address update illegal field city is processed correctly according to specification, preventing regressions.

### Passing Test 50: Loyalty Redeem Zero Points
- **Endpoint tested**: POST /api/v1/loyalty/redeem
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/loyalty/redeem
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'points': 0}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that loyalty redeem zero points is processed correctly according to specification, preventing regressions.

### Passing Test 51: Loyalty Redeem Negative Points
- **Endpoint tested**: POST /api/v1/loyalty/redeem
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/loyalty/redeem
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'points': -5}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that loyalty redeem negative points is processed correctly according to specification, preventing regressions.

### Passing Test 52: Order Cancel Non Existent
- **Endpoint tested**: POST /api/v1/orders/99999/cancel
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/orders/99999/cancel
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: None
- **Expected result**: 404 HTTP Status Code
- **Actual result observed**: 404 HTTP Status Code
- **Reason why this test case is useful**: Validates that order cancel non existent is processed correctly according to specification, preventing regressions.

### Passing Test 53: Ticket Create Short Subject
- **Endpoint tested**: POST /api/v1/support/ticket
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/support/ticket
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'subject': 'abc', 'message': 'Valid long message.'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that ticket create short subject is processed correctly according to specification, preventing regressions.

### Passing Test 54: Ticket Update Status Backward
- **Endpoint tested**: PUT /api/v1/support/tickets/99999
- **Request payload**:
  - Method: PUT
  - URL: http://localhost:8080/api/v1/support/tickets/99999
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'status': 'CLOSED'}
- **Expected result**: 404 HTTP Status Code
- **Actual result observed**: 404 HTTP Status Code
- **Reason why this test case is useful**: Validates that ticket update status backward is processed correctly according to specification, preventing regressions.

### Passing Test 55: Loyalty Negative Balance
- **Endpoint tested**: POST /api/v1/loyalty/redeem
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/loyalty/redeem
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'points': 99999}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that loyalty negative balance is processed correctly according to specification, preventing regressions.

### Passing Test 56: Ticket Injection
- **Endpoint tested**: POST /api/v1/support/ticket
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/support/ticket
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'subject': 'Test Ticket', 'message': "' OR 1=1; DROP TABLE tickets; --"}
- **Expected result**: 200 HTTP Status Code
- **Actual result observed**: 200 HTTP Status Code
- **Reason why this test case is useful**: Validates that ticket injection is processed correctly according to specification, preventing regressions.

### Passing Test 57: Profile Empty Payload
- **Endpoint tested**: PUT /api/v1/profile
- **Request payload**:
  - Method: PUT
  - URL: http://localhost:8080/api/v1/profile
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: None
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that profile empty payload is processed correctly according to specification, preventing regressions.

### Passing Test 58: Loyalty Float Points
- **Endpoint tested**: POST /api/v1/loyalty/redeem
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/loyalty/redeem
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'points': 10.5}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that loyalty float points is processed correctly according to specification, preventing regressions.

### Passing Test 59: Loyalty Redeem No Points Field
- **Endpoint tested**: POST /api/v1/loyalty/redeem
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/loyalty/redeem
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: None
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that loyalty redeem no points field is processed correctly according to specification, preventing regressions.

### Passing Test 60: Address Missing Label
- **Endpoint tested**: POST /api/v1/addresses
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/addresses
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'street': '123 Main St', 'city': 'Metropolis', 'pincode': '123456'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that address missing label is processed correctly according to specification, preventing regressions.

### Passing Test 61: Address Missing Street
- **Endpoint tested**: POST /api/v1/addresses
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/addresses
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'label': 'HOME', 'city': 'Metropolis', 'pincode': '123456'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that address missing street is processed correctly according to specification, preventing regressions.

### Passing Test 62: Address Missing City
- **Endpoint tested**: POST /api/v1/addresses
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/addresses
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'label': 'HOME', 'street': '123 Main St', 'pincode': '123456'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that address missing city is processed correctly according to specification, preventing regressions.

### Passing Test 63: Address Missing Pincode
- **Endpoint tested**: POST /api/v1/addresses
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/addresses
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'label': 'HOME', 'street': '123 Main St', 'city': 'Metropolis'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that address missing pincode is processed correctly according to specification, preventing regressions.

### Passing Test 64: Profile Update Missing Name
- **Endpoint tested**: PUT /api/v1/profile
- **Request payload**:
  - Method: PUT
  - URL: http://localhost:8080/api/v1/profile
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'phone': '1234567890'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that profile update missing name is processed correctly according to specification, preventing regressions.

### Passing Test 65: Profile Update Missing Phone
- **Endpoint tested**: PUT /api/v1/profile
- **Request payload**:
  - Method: PUT
  - URL: http://localhost:8080/api/v1/profile
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'name': 'John Doe'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that profile update missing phone is processed correctly according to specification, preventing regressions.

### Passing Test 66: Support Ticket Subject Too Long
- **Endpoint tested**: POST /api/v1/support/ticket
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/support/ticket
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'subject': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'message': 'My issue is detailed'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that support ticket subject too long is processed correctly according to specification, preventing regressions.

### Passing Test 67: Checkout Invalid Payment Method
- **Endpoint tested**: POST /api/v1/checkout
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/checkout
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'payment_method': 'INVALID'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that checkout invalid payment method is processed correctly according to specification, preventing regressions.

### Passing Test 68: Loyalty Redeem Non Integer Points
- **Endpoint tested**: POST /api/v1/loyalty/redeem
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/loyalty/redeem
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'points': 'two'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that loyalty redeem non integer points is processed correctly according to specification, preventing regressions.

### Passing Test 69: Loyalty Redeem Boolean Points
- **Endpoint tested**: POST /api/v1/loyalty/redeem
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/loyalty/redeem
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'points': True}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that loyalty redeem boolean points is processed correctly according to specification, preventing regressions.

### Passing Test 70: Loyalty Redeem Empty Points
- **Endpoint tested**: POST /api/v1/loyalty/redeem
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/loyalty/redeem
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'points': ''}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that loyalty redeem empty points is processed correctly according to specification, preventing regressions.

### Passing Test 71: Profile Update Long Name
- **Endpoint tested**: PUT /api/v1/profile
- **Request payload**:
  - Method: PUT
  - URL: http://localhost:8080/api/v1/profile
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'name': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'phone': '1234567890'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that profile update long name is processed correctly according to specification, preventing regressions.

### Passing Test 72: Profile Update Non String Name
- **Endpoint tested**: PUT /api/v1/profile
- **Request payload**:
  - Method: PUT
  - URL: http://localhost:8080/api/v1/profile
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'name': 123456, 'phone': '1234567890'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that profile update non string name is processed correctly according to specification, preventing regressions.

### Passing Test 73: Address Add Long Street
- **Endpoint tested**: POST /api/v1/addresses
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/addresses
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'label': 'HOME', 'street': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'city': 'Metropolis', 'pincode': '123456'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that address add long street is processed correctly according to specification, preventing regressions.

### Passing Test 74: Ticket Add Long Message
- **Endpoint tested**: POST /api/v1/support/ticket
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/support/ticket
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'subject': 'Need help', 'message': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that ticket add long message is processed correctly according to specification, preventing regressions.

### Passing Test 75: Loyalty Redeem Very Large Points
- **Endpoint tested**: POST /api/v1/loyalty/redeem
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/loyalty/redeem
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'points': 99999999999999999999999}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that loyalty redeem very large points is processed correctly according to specification, preventing regressions.

### Passing Test 76: Checkout Missing Payment Method
- **Endpoint tested**: POST /api/v1/checkout
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/checkout
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: None
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that checkout missing payment method is processed correctly according to specification, preventing regressions.

### Passing Test 77: Put Profile Without Name
- **Endpoint tested**: PUT /api/v1/profile
- **Request payload**:
  - Method: PUT
  - URL: http://localhost:8080/api/v1/profile
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'phone': '1314151617'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that put profile without name is processed correctly according to specification, preventing regressions.

### Passing Test 78: Delete Non Existent Address
- **Endpoint tested**: DELETE /api/v1/addresses/9999
- **Request payload**:
  - Method: DELETE
  - URL: http://localhost:8080/api/v1/addresses/9999
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: None
- **Expected result**: 404 HTTP Status Code
- **Actual result observed**: 404 HTTP Status Code
- **Reason why this test case is useful**: Validates that delete non existent address is processed correctly according to specification, preventing regressions.

### Passing Test 79: Review Integer Comment
- **Endpoint tested**: POST /api/v1/products/1/reviews
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/products/1/reviews
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'rating': 5, 'comment': 12345}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that review integer comment is processed correctly according to specification, preventing regressions.

### Passing Test 80: Cart Add Boolean Quantity
- **Endpoint tested**: POST /api/v1/cart/add
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/cart/add
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'product_id': 1, 'quantity': True}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that cart add boolean quantity is processed correctly according to specification, preventing regressions.

### Passing Test 81: Address Add Boolean City
- **Endpoint tested**: POST /api/v1/addresses
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/addresses
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'label': 'HOME', 'street': '123 Main St', 'city': True, 'pincode': '123456'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that address add boolean city is processed correctly according to specification, preventing regressions.

### Passing Test 82: Cart Add Negative Product Id
- **Endpoint tested**: POST /api/v1/cart/add
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/cart/add
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'product_id': -1, 'quantity': 1}
- **Expected result**: 404 HTTP Status Code
- **Actual result observed**: 404 HTTP Status Code
- **Reason why this test case is useful**: Validates that cart add negative product id is processed correctly according to specification, preventing regressions.

### Passing Test 83: Review Negative Rating
- **Endpoint tested**: POST /api/v1/products/1/reviews
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/products/1/reviews
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'rating': -5, 'comment': 'Good'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that review negative rating is processed correctly according to specification, preventing regressions.

### Passing Test 84: Loyalty Point Redemption String
- **Endpoint tested**: POST /api/v1/loyalty/redeem
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/loyalty/redeem
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'points': '10'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that loyalty point redemption string is processed correctly according to specification, preventing regressions.

### Passing Test 85: Get Ticket Non Existent
- **Endpoint tested**: GET /api/v1/support/tickets/999999
- **Request payload**:
  - Method: GET
  - URL: http://localhost:8080/api/v1/support/tickets/999999
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: None
- **Expected result**: 404 HTTP Status Code
- **Actual result observed**: 404 HTTP Status Code
- **Reason why this test case is useful**: Validates that get ticket non existent is processed correctly according to specification, preventing regressions.

### Passing Test 86: Update Ticket Non Existent
- **Endpoint tested**: PUT /api/v1/support/tickets/999999
- **Request payload**:
  - Method: PUT
  - URL: http://localhost:8080/api/v1/support/tickets/999999
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'status': 'CLOSED'}
- **Expected result**: 404 HTTP Status Code
- **Actual result observed**: 404 HTTP Status Code
- **Reason why this test case is useful**: Validates that update ticket non existent is processed correctly according to specification, preventing regressions.

### Passing Test 87: Reviews Empty Payload
- **Endpoint tested**: POST /api/v1/products/1/reviews
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/products/1/reviews
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: None
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that reviews empty payload is processed correctly according to specification, preventing regressions.

### Passing Test 88: Checkout Invalid Type Payment
- **Endpoint tested**: POST /api/v1/checkout
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/checkout
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'payment_method': 1234}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that checkout invalid type payment is processed correctly according to specification, preventing regressions.

### Passing Test 89: Checkout Long Payment Method
- **Endpoint tested**: POST /api/v1/checkout
- **Request payload**:
  - Method: POST
  - URL: http://localhost:8080/api/v1/checkout
  - Headers: {'X-Roll-Number': '2024101046', 'X-User-ID': '1'}
  - Body: {'payment_method': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'}
- **Expected result**: 400 HTTP Status Code
- **Actual result observed**: 400 HTTP Status Code
- **Reason why this test case is useful**: Validates that checkout long payment method is processed correctly according to specification, preventing regressions.

