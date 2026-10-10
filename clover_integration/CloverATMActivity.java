package com.p3lending.atm;

import android.os.Bundle;
import android.widget.Toast;
import com.clover.sdk.v3.connector.IPaymentConnector;
import com.clover.sdk.v3.connector.PaymentConnector;
import com.clover.sdk.v3.remotepay.AuthRequest;
import com.clover.sdk.v3.remotepay.CardEntryMethods;

/**
 * P3 Lending ATM - Clover Native App
 *
 * This Android app runs directly on the Clover device and:
 * - Uses Clover's secure card reader
 * - Uses secure PIN pad (PCI-compliant)
 * - Communicates with Flask backend
 * - Displays ATM interface on customer-facing display
 */
public class CloverATMActivity extends Activity {

    private IPaymentConnector paymentConnector;
    private static final String ATM_SERVER = "http://100.103.3.35:5050";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.atm_main);

        // Initialize Clover Payment Connector
        paymentConnector = new PaymentConnector(this,
            getAccount(),
            new PaymentConnectorListener());
        paymentConnector.initializeConnection();
    }

    /**
     * Request PIN entry on secure PIN pad
     */
    private void authenticateWithCard() {
        // Show message on customer display
        showCustomerMessage("Please insert card and enter PIN");

        // Create auth request for Clover
        AuthRequest request = new AuthRequest();
        request.setAmount(0L);  // $0 auth for PIN verification only
        request.setCardEntryMethods(
            CardEntryMethods.MANUAL |
            CardEntryMethods.MAG_STRIPE |
            CardEntryMethods.CHIP
        );
        request.setDisableCashback(true);
        request.setDisableRestartTransactionOnFail(false);

        // Request PIN on secure pad
        paymentConnector.auth(request);
    }

    /**
     * Handle successful PIN entry
     */
    private void onPinVerified(String encryptedPin, String cardToken) {
        // Send to Flask backend
        JSONObject payload = new JSONObject();
        payload.put("encrypted_pin", encryptedPin);
        payload.put("card_token", cardToken);

        OkHttpClient client = new OkHttpClient();
        RequestBody body = RequestBody.create(
            MediaType.parse("application/json"),
            payload.toString()
        );

        Request request = new Request.Builder()
            .url(ATM_SERVER + "/api/authenticate/card")
            .post(body)
            .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onResponse(Call call, Response response) {
                if (response.isSuccessful()) {
                    // Load ATM interface in WebView
                    loadATMInterface();
                } else {
                    showError("Authentication failed");
                }
            }

            @Override
            public void onFailure(Call call, IOException e) {
                showError("Connection error: " + e.getMessage());
            }
        });
    }

    /**
     * Load ATM interface in full-screen WebView
     */
    private void loadATMInterface() {
        WebView webView = findViewById(R.id.atm_webview);
        webView.getSettings().setJavaScriptEnabled(true);
        webView.getSettings().setDomStorageEnabled(true);
        webView.loadUrl(ATM_SERVER);

        // Make it feel like native app
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                view.loadUrl(url);
                return true;
            }
        });
    }

    /**
     * Show message on customer-facing display
     */
    private void showCustomerMessage(String message) {
        if (paymentConnector != null) {
            paymentConnector.showMessage(message);
        }
    }

    private class PaymentConnectorListener implements IPaymentConnectorListener {
        @Override
        public void onAuthResponse(AuthResponse response) {
            if (response.getSuccess()) {
                // PIN verified successfully
                onPinVerified(
                    response.getPayment().getCardTransaction().getEncryptedPan(),
                    response.getPayment().getCardTransaction().getToken()
                );
            } else {
                showError("PIN verification failed: " + response.getReason());
            }
        }

        @Override
        public void onDeviceConnected() {
            Toast.makeText(CloverATMActivity.this,
                "Clover device connected",
                Toast.LENGTH_SHORT).show();
        }

        @Override
        public void onDeviceDisconnected() {
            showError("Clover device disconnected");
        }
    }
}
