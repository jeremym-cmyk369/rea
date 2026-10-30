<?php
// AI Business Harness — contact form handler.
// Emails each inquiry to the inbox below. Stores nothing on the server.
declare(strict_types=1);

const TO_ADDRESS   = 'jeremy@aibusinessharness.com';
const FROM_ADDRESS = 'jeremy@aibusinessharness.com';
const SITE_NAME    = 'AI Business Harness';

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');

function respond(int $code, bool $ok, string $message): void {
    http_response_code($code);
    echo json_encode(['ok' => $ok, 'message' => $message]);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    respond(405, false, 'Method not allowed.');
}

// Only accept submissions from this site's own pages.
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
$host   = $_SERVER['HTTP_HOST'] ?? '';
if ($origin !== '' && parse_url($origin, PHP_URL_HOST) !== $host) {
    respond(403, false, 'Invalid request origin.');
}

// Honeypot: real visitors never see or fill this field.
if (trim((string)($_POST['website'] ?? '')) !== '') {
    respond(200, true, 'Thanks — your inquiry was sent.');
}

// Reject forms submitted faster than a human could type them.
$started = (int)($_POST['started'] ?? 0);
if ($started > 0 && (time() * 1000 - $started) < 3000) {
    respond(400, false, 'Please take a moment and try again.');
}

function field(string $name, int $max): string {
    $value = trim((string)($_POST[$name] ?? ''));
    $value = preg_replace('/[^\P{C}\n\t]/u', '', $value) ?? '';
    return mb_substr($value, 0, $max);
}
function header_safe(string $value): string {
    return trim(preg_replace('/[\r\n]+/', ' ', $value) ?? '');
}

$name    = header_safe(field('name', 120));
$email   = header_safe(field('email', 180));
$company = header_safe(field('company', 160));
$task    = field('task', 1200);

if ($name === '' || $task === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    respond(422, false, 'Please fill in your name, a valid email, and the task.');
}

// Basic per-IP throttle: max 5 submissions per 10 minutes.
$ip     = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
$bucket = sys_get_temp_dir() . '/abh_contact_' . hash('sha256', $ip);
$now    = time();
$hits   = array_filter(
    is_file($bucket) ? (array)json_decode((string)@file_get_contents($bucket), true) : [],
    fn($t) => is_int($t) && $t > $now - 600
);
if (count($hits) >= 5) {
    respond(429, false, 'Too many submissions. Please email us directly instead.');
}
$hits[] = $now;
@file_put_contents($bucket, json_encode(array_values($hits)), LOCK_EX);

$subject = SITE_NAME . ' inquiry — ' . ($company !== '' ? $company : $name);
$body = implode("\n", [
    'New inquiry from the ' . SITE_NAME . ' website',
    '',
    'Name:    ' . $name,
    'Email:   ' . $email,
    'Company: ' . ($company !== '' ? $company : 'Not provided'),
    '',
    'What task keeps repeating?',
    $task,
    '',
    '—',
    'Sent ' . gmdate('Y-m-d H:i') . ' UTC from ' . ($_SERVER['HTTP_REFERER'] ?? 'aibusinessharness.com'),
    'Reply to this email to respond directly to ' . $name . '.',
]);

$headers = [
    'From: ' . SITE_NAME . ' <' . FROM_ADDRESS . '>',
    'Reply-To: =?UTF-8?B?' . base64_encode($name) . '?= <' . $email . '>',
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
];

$sent = mail(
    TO_ADDRESS,
    '=?UTF-8?B?' . base64_encode($subject) . '?=',
    $body,
    implode("\r\n", $headers),
    '-f' . FROM_ADDRESS
);

if (!$sent) {
    respond(500, false, 'We couldn\'t send your inquiry. Please email ' . TO_ADDRESS . ' directly.');
}

respond(200, true, 'Thanks — your inquiry was sent. We\'ll reply by email.');
