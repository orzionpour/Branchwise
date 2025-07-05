package com.example.aicodereviewer.webhook.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Mono;

import java.util.Map;

@RestController
@RequestMapping("/api/v1/webhooks/github")
public class GithubWebhookController {

    private static final Logger logger = LoggerFactory.getLogger(GithubWebhookController.class);

    // Define constants for GitHub event headers
    private static final String GITHUB_EVENT_HEADER = "X-GitHub-Event";
    private static final String GITHUB_DELIVERY_HEADER = "X-GitHub-Delivery"; // Unique ID for the event
    private static final String GITHUB_SIGNATURE_HEADER = "X-Hub-Signature-256"; // For payload verification

    @PostMapping("/events")
    public Mono<ResponseEntity<String>> handleGithubWebhook(
            @RequestBody String payload,
            @RequestHeader(GITHUB_EVENT_HEADER) String githubEvent,
            @RequestHeader(GITHUB_DELIVERY_HEADER) String githubDelivery,
            @RequestHeader(value = GITHUB_SIGNATURE_HEADER, required = false) String signature) {

        logger.info("Received GitHub Webhook Event: {}", githubEvent);
        logger.info("Delivery ID: {}", githubDelivery);
        logger.info("Signature: {}", signature != null ? signature : "Not provided");
        logger.info("Payload: {}", payload);

        // Basic event handling logic (will be expanded)
        // For now, we just acknowledge receipt.
        // Later, we will parse the payload into a DTO, verify the signature,
        // and publish an event to a message queue.

        if ("ping".equalsIgnoreCase(githubEvent)) {
            logger.info("Responding to GitHub ping event");
            return Mono.just(ResponseEntity.ok("Pong! Ping event received successfully."));
        } else if ("pull_request".equalsIgnoreCase(githubEvent)) {
            // TODO: Process pull request event
            // For now, just log and return OK
            logger.info("Processing pull_request event...");
            // Actual processing will involve pushing to a queue
        } else {
            logger.warn("Received unhandled event type: {}", githubEvent);
            return Mono.just(ResponseEntity.status(HttpStatus.ACCEPTED).body("Event received but not specifically processed."));
        }

        return Mono.just(ResponseEntity.ok("Event received successfully."));
    }
}
